exports.up = function (knex) {
    return knex.schema.createTable('round_setup', (table) => {
        table.increments('id').primary(); // Auto-increment primary key column
        table.integer('roundIndex').notNullable().unique();
        table.integer('ntrials').notNullable();
        table.string('firstplayer', 50).notNullable();
        table.string('easy_defect', 50).notNullable();
        table.integer('chick_startstate').notNullable();
        table.integer('agent1_startstate').notNullable();
        table.integer('agent2_startstate').notNullable();
        table.integer('chick_startx').notNullable();
        table.integer('chick_starty').notNullable();
        table.integer('agent1_startx').notNullable();
        table.integer('agent1_starty').notNullable();
        table.integer('agent2_startx').notNullable();
        table.integer('agent2_starty').notNullable();
        table.float('chick_to_1').notNullable();
        table.float('chick_to_2').notNullable();
        table.float('chick_to_both').notNullable();
        table.timestamps(true, true); // Adds 'created_at' and 'updated_at' columns
    });
};

exports.down = function (knex) {
    return knex.schema.dropTable('round_setup');
};
