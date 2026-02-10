# Egghunt Online

## How to Run the Client Locally

1. Make sure you are in the root directory of the project.
2. add a .env.local file at the root of the project with the following:

    `VITE_SERVER_PORT=8000`
    
    where 8000 is the port the server will be running on

3. run `$ npm install`
4. run `$ npm run dev`
5. the client should now be running on http://localhost:5173/

To stop the client, enter `q` in the terminal that the client is running in.

## How to set up the database locally
### NOTE: The database must be set up before the server.

#### Download MYSQL for your operating system 

- Windows: https://dev.mysql.com/doc/refman/8.0/en/windows-installation.html
- Mac: https://dev.mysql.com/doc/refman/8.0/en/macos-installation.html

#### Setup the environment variables for this project
1. create an `.env` file at the root of the project.
2. paste the following into the `.env` file, replacing your username (usually root) and password
```
DB_HOST=127.0.0.1
DB_NAME=egghunt_dev
DB_USER=root
DB_PASSWORD=your_password_here
```

#### Create the database, migrate the tables, and seed the round_results table
1. create a new database locally called `egghunt_dev` via the mysql command line.
2. run `$ npm run migrate`
3. run `$ npm run seed`

You can download [this](https://marketplace.visualstudio.com/items?itemName=cweijan.vscode-mysql-client2) VSCode extension to view your databases. 
## How to Run the Server Locally

0. Open a new terminal window (don't use the terminal window the client is running in)
1. Make sure you are in the root directory of the project.
2. check that you are using node version `18.15.0` using the command `$ node -v`
    
    you can optionally install [nvm](https://github.com/nvm-sh/nvm) and run `$ nvm use`.

3. run `$ npm run build`. This builds the client in a folder called /frontend_build.
4. run `$ npm run build:server`. This compiles the server from Typescript to Javascript in a folder called /server_build.
5. run `$ npm run start:server`. This starts the server using node. 
6. the server should now be running on http://localhost:8000/

To stop the server, press `Ctrl+C` in the terminal that the server is running in.
## Notes on Workflow

- If you change the server.ts file, it needs to be be rebuilt using `$ npm run build:server`. Stop and restart the server using `Ctrl+C` and then `$ npm run start:server`.
- If you change the EgghuntGame.tsx file, the server also needs to be rebuilt as it imports that file.
- In production, both the client and the server will be running on the same port using `$ npm run start`. When developing locally, in order to take advantage of vite's development features, we suggest running the client and the server separately. 
- If you are testing a game locally and see "existing game found" when you go to /tasks/egghunt/join, or want to start with a fresh game, clear the Local Storage in your browser in the Application tab of Developer Tools.
- When developing locally, if the server restarts for any reason, any in-progress games will become invalid and you may see "connecting..." text on the screen. To start a new game, clear local storage.

## Deployment

- This repository is connected to two Heroku projects- `egghunt` and `egghunt-stag`
- Both have one basic dyno of type "web" that is set to run `npm start`, which starts both the client and server. Both are using JawsDB MySQL under the free Kitefin shared plan.
- The production URL is at https://egghunt.herokuapp.com/
- The staging URL is at https://egghunt-staging-155c6f73cf2a.herokuapp.com/
- `egghunt-stag` is set to automatically deploy when there are updates to the main branch.
- `egghunt` (production) will NOT automatically deploy. All deploys need to be trigged manually.
- All testing should occur on `egghunt-stag` to not polute the production database.
- When new database migrations are needed (i.e. new Knex migration files are created), the migrations need to be done MANUALLY on both `egghunt` and `egghunt-stag`. To do so, use the "run console" feature in Heroku to run the `bash` console. In the console, run `npm run migrate` to make migrations on the JawsDB database.
## Technologies used

- bootstrapped using [vite](https://vitejs.dev/) (React + Typescript)
- [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)
- [boardgame.io](https://boardgame.io/)
