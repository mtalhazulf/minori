<template>
  <q-item
    v-if="auth.includes(operator.usertype)"
    clickable
    tag="a"
    target="_blank"
    @click="to ? $router.push(to) : redirect(redirect_to)">
    <q-item-section v-if="icon" avatar>
      <q-icon :name="icon" />
    </q-item-section>

    <q-item-section>
      <q-item-label>{{ title }}</q-item-label>
      <q-item-label caption>
        {{ caption }}
      </q-item-label>
    </q-item-section>
  </q-item>
</template>

<script>
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'EssentialLink',
  props: {
    title: {
      type: String,
      required: true
    },

    caption: {
      type: String,
      default: ''
    },

    to: {
      type: String,
      default: ''
    },
    redirect_to: {
      type: String,
      default: ''
    },
    link: {
      type: String
    },

    icon: {
      type: String,
      default: ''
    },

    auth: {
      type: Array
    }
  },
  data() {
    return {
      operator: ''
    }
  },
  mounted() {
    this.operator = JSON.parse(sessionStorage.getItem('user'))
  },
  methods: {
    redirect(url) {
      window.location.href =
        url + '?jwt=' + sessionStorage.getItem('access-token')
    }
  }
})
</script>

<style scoped>
.q-item {
  margin-top: 5px;
  font-size: smaller;
}
</style>
