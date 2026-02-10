/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
exports.up = function (knex) {
    return knex.schema.alterTable("moves", (table) => {
        table.unique(["temp_trial_id", "player", "action"]);
    });
};

/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
exports.down = function (knex) {
    return knex.schema.alterTable("moves", (table) => {
        table.dropUnique(["temp_trial_id", "player", "action"]);
    });
};
