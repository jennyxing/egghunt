/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
exports.up = function (knex) {
    return knex.schema.alterTable("trials", (table) => {
        table.unique(["match_id", "agent1_pts", "agent2_pts"]);
    });
};

/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
exports.down = function (knex) {
    return knex.schema.alterTable("trials", (table) => {
        table.dropUnique(["match_id", "agent1_pts", "agent2_pts"]);
    });
};
