const template = await fetch("/templates/_challenge_rules.html").then((r) =>
    r.text(),
);

export default {
    template: template,
};
