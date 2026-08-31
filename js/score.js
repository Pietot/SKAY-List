/**
 * Calculate the score awarded when having a certain percentage on a list level
 * @param {Number} rank Position on the list
 * @returns {Number}
 */
export function score(rank) {
    if (rank > 150) {
        return 0;
    }

    let k = 0.4;
    let x = 150;
    let score = (x / (Math.pow(x, k) + 1 - Math.pow(x / rank, k))) ^ (1 / k);

    return Math.round(score);
}
