/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
exports.up = function (knex) {
    return knex.schema.createTable("matches", (table) => {
        table.increments("match_id").primary();
        table.integer("game_id")
            .unsigned()
            .references("games.game_id")
            .onUpdate('CASCADE')
            .onDelete('CASCADE');
        table.integer("round_index")
            .references("round_setup.roundIndex")
            .onUpdate('CASCADE')
            .onDelete('CASCADE');
        table.string("bgio_match_id");
        table.timestamps(true, true);
    })
};

/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
exports.down = function (knex) {
    return knex.schema.dropTable("matches")
};
