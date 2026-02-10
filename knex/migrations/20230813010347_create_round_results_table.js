/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
exports.up = function (knex) {
    return knex.schema.createTable("round_results", (table) => {
        table.increments("round_result_id").primary();
        table.integer("match_id")
            .unsigned()
            .references("matches.match_id")
            .onUpdate('CASCADE')
            .onDelete('CASCADE');
        table.integer("agent1_score").notNullable();
        table.integer("agent2_score").notNullable();
        table.integer("total_trials").notNullable();
        table.timestamps(true, true);
    })
};

/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
exports.down = function (knex) {
    return knex.schema.dropTable("round_results")
};
