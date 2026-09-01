import { store } from "../main.js";
import { embed } from "../util.js";
import { score } from "../score.js";
import { fetchEditors, fetchList } from "../content.js";
import { getLevelStatAverage, formatStatValue } from "../stats.js";

import ChallengeRules from "./ChallengeRules.js";
import ExtremeRules from "./ExtremeRules.js";
import Spinner from "../components/Spinner.js";
import LevelAuthors from "../components/List/LevelAuthors.js";

const roleIconMap = {
    owner: "crown",
    admin: "user-gear",
    helper: "user-shield",
    dev: "code",
    trial: "user-lock",
};

const template = await fetch("/templates/List.html").then((response) =>
    response.text(),
);

export default {
    components: { Spinner, LevelAuthors, ChallengeRules, ExtremeRules },
    props: {
        listType: {
            type: String,
            default: "challenges",
        },
    },
    template: template,
    data: () => ({
        list: [],
        editors: [],
        loading: true,
        selected: 0,
        errors: [],
        roleIconMap,
        store,
    }),
    computed: {
        level() {
            return this.list[this.selected][0];
        },
        isYoutubeVideo() {
            const url = this.level?.verification || "";
            return /(?:youtu\.be|youtube\.com)/i.test(url);
        },
        video() {
            if (!this.level) {
                return "";
            }

            const verification = this.level.verification || "";

            if (/(?:youtu\.be|youtube\.com)/i.test(verification)) {
                return embed(verification);
            }

            return verification;
        },
        levelAverageEnjoyment() {
            if (this.listType !== "challenges") {
                return null;
            }
            return getLevelStatAverage(this.level, "enjoyment");
        },
        levelAverageAttempts() {
            if (this.listType !== "challenges") {
                return null;
            }
            return getLevelStatAverage(this.level, "attempts");
        },
    },
    async mounted() {
        await this.loadList();
    },
    watch: {
        listType: {
            immediate: true,
            handler() {
                this.loadList();
            },
        },
    },
    methods: {
        async loadList() {
            this.loading = true;
            this.selected = 0;
            this.errors = [];
            this.list = [];

            this.list = await fetchList(this.listType);
            this.editors = await fetchEditors();

            // Error handling
            if (!this.list) {
                this.errors = [
                    "Failed to load list. Retry in a few minutes or notify list staff.",
                ];
            } else {
                this.errors.push(
                    ...this.list
                        .filter(([_, err]) => err)
                        .map(([_, err]) => {
                            return `Failed to load level. (${err}.json)`;
                        }),
                );
                if (!this.editors) {
                    this.errors.push("Failed to load list editors.");
                }
            }

            this.loading = false;
        },
        embed,
        score,
        formatStatValue,
    },
};
