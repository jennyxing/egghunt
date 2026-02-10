/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
exports.up = function (knex) {
    return knex.schema.createTable("games", (table) => {
        table.increments("game_id").primary();
        table.string("player1_study_id").notNullable();
        table.string("player2_study_id").notNullable();
        table.string("chicken_id").notNullable().defaultTo("chicken");
        table.timestamps(true, true);
    })
};

/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
exports.down = function (knex) {
    return knex.schema.dropTable("games")
};
