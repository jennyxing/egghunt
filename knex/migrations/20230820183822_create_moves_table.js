/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
exports.up = function (knex) {
    return knex.schema.createTable("moves", (table) => {
        table.increments("move_id").primary();
        table.integer("trial_id")
            .unsigned()
            .references("trials.trial_id")
            .onUpdate('CASCADE')
            .onDelete('CASCADE');
        table.string("player").notNullable(); //either chick1, agent1, or agent2
        table.string("action").notNullable(); //either up, down, left, right, or stay
        table.integer("x").notNullable(); //the new location the player or chicken moved to
        table.integer("y").notNullable(); //the new location the player or chicken moved to
        table.timestamps(true, true);
    })
};

/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
exports.down = function (knex) {
    return knex.schema.dropTable("moves")
};
