import { score } from "./score.js";

/**
 * Path to directory containing the list metadata files and all levels.
 */
const dir = "/data";

const listFileByType = {
    challenges: "_challenge_list.json",
    extremes: "_extreme_list.json",
};

export async function fetchList(listType = "challenges") {
    const listFile = listFileByType[listType] ?? listFileByType.challenges;
    const listResult = await fetch(`${dir}/${listFile}`);

    try {
        const list = await listResult.json();
        const subDir = listType === "challenges" ? `/challenges` : `/extremes`;
        return await Promise.all(
            list.map(async (path, rank) => {
                const levelResult = await fetch(
                    `${dir}/${subDir}/${path}.json`,
                );
                try {
                    const level = await levelResult.json();
                    return [
                        {
                            ...level,
                            path,
                            records: level.records,
                        },
                        null,
                    ];
                } catch {
                    console.error(`Failed to load level #${rank + 1} ${path}.`);
                    return [null, path];
                }
            }),
        );
    } catch {
        console.error(`Failed to load list: ${listFile}`);
        return null;
    }
}

export async function fetchEditors() {
    try {
        const editorsResults = await fetch(`${dir}/_editors.json`);
        const editors = await editorsResults.json();
        return editors;
    } catch {
        return null;
    }
}

export async function fetchLeaderboard(listType = "challenges") {
    const list = await fetchList(listType);
    if (!Array.isArray(list)) {
        return [[], []];
    }

    const scoreMap = {};
    const errs = [];

    list.forEach(([level, err], rank) => {
        if (err || !level) {
            if (err) {
                errs.push(err);
            }
            return;
        }

        if (listType === "challenges") {
            const verifier =
                Object.keys(scoreMap).find(
                    (u) =>
                        u.toLowerCase() ===
                        (level.verifier || "").toLowerCase(),
                ) ||
                level.verifier ||
                "Unknown";
            scoreMap[verifier] ??= {
                verified: [],
                completed: [],
            };

            const { verified } = scoreMap[verifier];
            verified.push({
                rank: rank + 1,
                level: level.name,
                score: score(rank + 1),
                link: level.verification,
            });
        }

        (level.records || []).forEach((record) => {
            const user =
                Object.keys(scoreMap).find(
                    (u) =>
                        u.toLowerCase() === (record.user || "").toLowerCase(),
                ) || record.user;
            scoreMap[user] ??= {
                verified: [],
                completed: [],
            };

            const { completed } = scoreMap[user];
            completed.push({
                rank: rank + 1,
                level: level.name,
                score:
                    listType === "challenges"
                        ? score(rank + 1)
                        : level.aredl_points,
                link: record.link,
            });
            return;
        });
    });

    const res = Object.entries(scoreMap).map(([user, scores]) => {
        console.log(user, scores);
        const { verified, completed } = scores;
        const total = [verified, completed]
            .flat()
            .reduce((prev, cur) => prev + cur.score, 0);

        return {
            user,
            total: Math.round((total + Number.EPSILON) * 100) / 100,
            ...scores,
        };
    });

    return [res.sort((a, b) => b.total - a.total), errs];
}
