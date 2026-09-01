export default {
    props: {
        author: {
            type: String,
            required: true,
        },
        creators: {
            type: Array,
            required: true,
        },
        verifier: {
            type: String,
            required: true,
        },
        listType: {
            type: String,
            required: true,
        },
        attempts: {
            type: [Number, String],
            default: null,
        },
        enjoyment: {
            type: [Number, String],
            default: null,
        },
    },
    template: `
        <div class="level-authors">
            <template v-if="selfVerified">
                <div class="type-title-sm">Creator & Verifier</div>
                <p class="type-body">
                    <span>{{ author }}</span>
                </p>
            </template>
            <template v-else-if="creators.length === 0">
                <div class="type-title-sm">Creator</div>
                <p class="type-body">
                    <span>{{ author }}</span>
                </p>
                <div class="type-title-sm">Verifier</div>
                <p class="type-body">
                    <span>{{ verifier }}</span>
                </p>
            </template>
            <template v-else>
                <div class="type-title-sm">Creators</div>
                <p class="type-body">
                    <template v-for="(creator, index) in creators" :key="\`creator-\$\{creator\}\`">
                        <span >{{ creator }}</span
                        ><span v-if="index < creators.length - 1">, </span>
                    </template>
                </p>
                <div class="type-title-sm">Verifier</div>
                <p class="type-body">
                    <span>{{ verifier }}</span>
                </p>
            </template>
            <div class="type-title-sm">Publisher</div>
            <p class="type-body">
                <span>{{ author }}</span>
            </p>
            <div v-if="listType === 'challenges'" class="type-title-sm">Attempts</div>
            <p v-if="listType === 'challenges'" class="type-body">
                <span>{{ attemptsText }}</span>
            </p>
            <div v-if="listType === 'challenges'" class="type-title-sm">Enjoyment</div>
            <p v-if="listType === 'challenges'" class="type-body">
                <span>{{ enjoymentText }}</span>
            </p>
        </div>
    `,

    computed: {
        selfVerified() {
            return this.author === this.verifier && this.creators.length === 0;
        },
        attemptsText() {
            return this.attempts === null ||
                this.attempts === undefined ||
                this.attempts === ""
                ? "-"
                : this.attempts;
        },
        enjoymentText() {
            return this.enjoyment === null ||
                this.enjoyment === undefined ||
                this.enjoyment === ""
                ? "-"
                : `${this.enjoyment}/10`;
        },
    },
};
