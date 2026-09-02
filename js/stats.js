export function getAvailableAverage(values = []) {
    const valid = (values || [])
        .filter(
            (value) => value !== null && value !== undefined && value !== "",
        )
        .map((value) => Number(value));

    if (valid.length === 0) {
        return null;
    }

    const total = valid.reduce((sum, value) => sum + value, 0);
    return Number((total / valid.length).toFixed(2));
}

export function getLevelStatAverage(level, key) {
    if (!level) {
        return null;
    }

    const directValue = level[key];
    const hasDirectValue =
        directValue !== null && directValue !== undefined && directValue !== "";

    if (hasDirectValue && !level.records) { 
        return Number(directValue);
    }

    if (!Array.isArray(level.records)) {
        return null;
    }

    const values = [
        ...(hasDirectValue ? [directValue] : []),
        ...level.records
            .map((record) => record?.[key])
            .filter(
                (value) =>
                    value !== null && value !== undefined && value !== "",
            ),
    ];

    return values.length > 0 ? getAvailableAverage(values) : null;
}

export function formatStatValue(value, suffix = "") {
    if (value === null || value === undefined || value === "") {
        return "-";
    }

    const formatted =
        typeof value === "number" ? value.toString() : String(value);
    return `${formatted}${suffix}`;
}
