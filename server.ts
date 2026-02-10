import 'dotenv/config';
import { Server, Origins } from 'boardgame.io/server';
import path from 'path';
import serve from 'koa-static';
import { EgghuntGame } from './src/game-logic/EgghuntGame';
import type { Server as ServerTypes } from "boardgame.io";
import { FifoMatchmaker } from 'matchmaking';
import { koaBody } from 'koa-body';
import knex from 'knex';
//@ts-ignore
import knexfile from "../knexfile.js"

const knexInstance = knex(knexfile);

// Build path relative to the server_build/server.js file
const frontEndAppBuildPath = path.resolve(__dirname, '../frontend_build');
const PORT = process.env.PORT == null ? 8000 : parseInt(process.env.PORT);

let serverUrl: string;

let resolveWithMatchID: (value: string | PromiseLike<string>) => void;
let rejectMatchIDPromise: (reason?: any) => void;
let matchIDPromise: Promise<string> = new Promise((resolve, reject) => {
  resolveWithMatchID = resolve;
  rejectMatchIDPromise = reject;
});

const authenticateCredentials: ServerTypes.AuthenticateCredentials = (credentials, playerMetadata) => {
  if (!playerMetadata) {
    return false;
  }
  if (credentials === playerMetadata.credentials) {
    return true;
  }
  return false;
}

function generateRandomRoundOrder() {
  const roundIndices = new Array(24);
  // populate the array with numbers 1-24, inclusive
  for (let i = 0; i < 24; i++) {
    roundIndices[i] = i + 1;
  }
  //shuffle the array using the fisher-yates algorithm
  for (let i = 23; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [roundIndices[i], roundIndices[j]] = [roundIndices[j], roundIndices[i]];
  }

  return roundIndices;
}

async function runGame(players: any[]) {
  try {
    const [newGameID] = await knexInstance('games')
      .insert({
        player1_study_id: players[0].studyID,
        player2_study_id: players[1].studyID
      })
    const roundIndexOrder = generateRandomRoundOrder();
    for (const roundIndex of roundIndexOrder) {
      await knexInstance('matches').insert({
        game_id: newGameID,
        round_index: roundIndex
      })
    }
    const { round_index: firstRoundIndex } = await knexInstance('matches')
      .select('round_index')
      .where('game_id', newGameID)
      .whereNull('bgio_match_id')
      .first();
    const setupData = await knexInstance('round_setup')
      .select('ntrials',
        'firstplayer',
        'chick_startx',
        'chick_starty',
        'agent1_startx',
        'agent1_starty',
        'agent2_startx',
        'agent2_starty')
      .where('roundIndex', firstRoundIndex)
      .first();
    const { matchID } = await (await fetch(
      `${serverUrl}/games/egghunt/create`,
      {
        method: 'POST',
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          numPlayers: 2,
          setupData: setupData,
          unlisted: process.env.UNLIST_MATCHES
        })
      }
    )).json()
    await knexInstance('matches')
      .where({ game_id: newGameID, round_index: firstRoundIndex })
      .update({
        bgio_match_id: matchID,
        updated_at: knexInstance.fn.now()
      })
    resolveWithMatchID(matchID);
    // "reset" the promise for the next game that gets created
    matchIDPromise = new Promise((resolve, reject) => {
      resolveWithMatchID = resolve;
    });
  } catch (e) {
    rejectMatchIDPromise(e)
  }
}

function getKey(player: any) {
  return player.studyID;
}

let matchmaker = new FifoMatchmaker(runGame, getKey, { checkInterval: 2000 });

const server = Server({
  games: [EgghuntGame],
  origins: [Origins.LOCALHOST, 'https://egghunt.herokuapp.com'],
  authenticateCredentials
});

server.router.post('/tasks/egghunt/join-queue', koaBody(), async (ctx, next) => {
  serverUrl = `${ctx.protocol}://${ctx.host}`;
  matchmaker.push(ctx.request.body);

  try {
    const matchID = await matchIDPromise;
    ctx.body = {
      matchID
    }
    await next();
  } catch (e) {
    matchmaker.leaveQueue(ctx.request.body)
    console.log("ERROR in /join-queue: ", e)
  }
});

server.router.patch('/tasks/egghunt/leave-queue', koaBody(), async (ctx) => {
  matchmaker.leaveQueue(ctx.request.body)
  ctx.body = {
    message: "successfully left queue"
  }
});

server.router.get('/tasks/egghunt/round_setup', async (ctx) => {
  const { game_id: existingGameID, match_id } = await knexInstance('matches')
    .select('game_id', 'match_id')
    .where('bgio_match_id', ctx.query.currentBGIOMatchID)
    .first();
  const nextRoundIndex = await knexInstance('matches')
    .select('round_index')
    .where('game_id', existingGameID)
    .where('match_id', match_id + 1)
    .first();

  if (nextRoundIndex) {
    // there are more rounds to play
    const setupData = await knexInstance('round_setup')
      .select('ntrials',
        'firstplayer',
        'chick_startx',
        'chick_starty',
        'agent1_startx',
        'agent1_starty',
        'agent2_startx',
        'agent2_starty')
      .where('roundIndex', nextRoundIndex.round_index)
      .first();
    ctx.body = {
      setupData: setupData,
      round_index: nextRoundIndex.round_index,
      game_id: existingGameID,
      message: "next round found"
    }
  } else {
    //all 24 rounds have been played
    ctx.body = {
      message: "game finished"
    }
  }

})

server.router.patch('/tasks/egghunt/matches', koaBody(), async (ctx) => {
  const { game_id, round_index } = ctx.query;

  const existingMatchWithBGIOMatchID = await knexInstance("matches")
    .where("bgio_match_id", ctx.request.body.bgio_match_id)
    .first();
  if (existingMatchWithBGIOMatchID) {
    ctx.body = {
      message: "match with new bgio_match_id already updated"
    }
  } else {
    await knexInstance("matches").where({ game_id, round_index })
      .update({
        bgio_match_id: ctx.request.body.bgio_match_id,
        updated_at: knexInstance.fn.now()
      });
    ctx.body = {
      message: "successfully updated bgio_match_id"
    }
  }

});

server.router.post("/tasks/egghunt/round_results", koaBody(), async (ctx) => {
  try {
    const {
      agent1_pts,
      agent2_pts,
      bgio_match_id,
      total_trials
    } = ctx.request.body;
    const { game_id: existingGameID, match_id: currentMatchID } = await knexInstance('matches')
      .select('game_id', 'match_id',)
      .where('bgio_match_id', bgio_match_id)
      .first();

    const previousMatchID = await knexInstance('matches')
      .select('match_id')
      .where('game_id', existingGameID)
      .where('match_id', currentMatchID - 1)
      .first();
    if (previousMatchID) {
      // add new agent points to their previous cumulative scores
      const { agent1_score: previous_agent1_score, agent2_score: previous_agent2_score } = await knexInstance('round_results')
        .select('agent1_score', 'agent2_score')
        .where('match_id', previousMatchID.match_id)
        .first();

      await knexInstance('round_results')
        .insert({
          match_id: currentMatchID,
          agent1_score: previous_agent1_score + agent1_pts,
          agent2_score: previous_agent2_score + agent2_pts,
          total_trials: total_trials,
        }).onConflict().merge();

      ctx.body = {
        match_id: currentMatchID,
        agent1_score: previous_agent1_score + agent1_pts,
        agent2_score: previous_agent2_score + agent2_pts
      }
    } else {
      await knexInstance('round_results')
        .insert({
          match_id: currentMatchID,
          agent1_score: agent1_pts,
          agent2_score: agent2_pts,
          total_trials: total_trials,
        }).onConflict().merge();

      ctx.body = {
        match_id: currentMatchID,
        agent1_score: agent1_pts,
        agent2_score: agent2_pts
      }
    }
  } catch (error) {
    console.log(error)
  }
})

server.router.post("/tasks/egghunt/trials", koaBody(), async (ctx) => {
  try {
    const {
      agent1_pts,
      agent2_pts,
      outcome,
      trial_number,
      bgio_match_id,
    } = ctx.request.body;
    const { match_id: currentMatchID } = await knexInstance('matches')
      .select('match_id')
      .where('bgio_match_id', bgio_match_id)
      .first();

    let [newTrialID] = await knexInstance('trials')
      .insert({
        match_id: currentMatchID,
        agent1_pts: agent1_pts,
        agent2_pts: agent2_pts,
        outcome: outcome
      }).onConflict(["match_id", "agent1_pts", "agent2_pts"]).ignore();

    if (newTrialID === 0) {
      const { trial_id: foundTrialID } = await knexInstance('trials')
        .select('trial_id')
        .where({
          match_id: currentMatchID,
          agent1_pts: agent1_pts,
          agent2_pts: agent2_pts,
          outcome: outcome
        })
        .first();
      newTrialID = foundTrialID;
    }
    //update the moves table with the new trial id that's generated after 3 moves
    await knexInstance("moves").where({ temp_trial_id: `${bgio_match_id}_${trial_number}` })
      .update({
        trial_id: newTrialID,
        updated_at: knexInstance.fn.now()
      });
    ctx.body = {
      match_id: currentMatchID,
      agent1_score: agent1_pts,
      agent2_score: agent2_pts,
      outcome: outcome
    }
  } catch (error) {
    console.log(error)
  }
})

server.router.post("/tasks/egghunt/moves", koaBody(), async (ctx) => {
  try {
    const {
      trial_number,
      action,
      player,
      x,
      y,
      bgio_match_id,
    } = ctx.request.body;

    await knexInstance('moves')
      .insert({
        temp_trial_id: `${bgio_match_id}_${trial_number}`,
        player: player,
        action: action,
        x: x,
        y: y
      }).onConflict(["trial_id", "player", "action"]).ignore();

    ctx.body = {
      temp_trial_id: `${bgio_match_id}_${trial_number}`,
      player: player,
      action: action,
      x: x,
      y: y
    }
  } catch (error) {
    console.log(error)
  }
})

server.app.use(serve(frontEndAppBuildPath))

server.run(PORT, () => {
  server.app.use(
    async (ctx, next) => await serve(frontEndAppBuildPath)(
      Object.assign(ctx, { path: 'index.html' }),
      next
    )
  )
});