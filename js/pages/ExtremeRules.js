const template = await fetch("templates/_extreme_rules.html").then((r) =>
    r.text(),
);

export default {
    template: template,
};
