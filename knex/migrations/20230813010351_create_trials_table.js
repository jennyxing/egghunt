/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
exports.up = function (knex) {
    return knex.schema.createTable("trials", (table) => {
        table.increments("trial_id").primary();
        table.integer("match_id")
            .unsigned()
            .references("matches.match_id")
            .onUpdate('CASCADE')
            .onDelete('CASCADE');
        table.integer("agent1_pts").notNullable(); //number of points the player has at the end of the trial
        table.integer("agent2_pts").notNullable(); //number of points the player has at the end of the trial
        table.string("outcome").notNullable(); //either none, "agent1 defect", or "agent2 defect"
        table.timestamps(true, true);
    })
};

/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
exports.down = function (knex) {
    return knex.schema.dropTable("trials")
};
