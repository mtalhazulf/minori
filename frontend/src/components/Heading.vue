<template>
  <h5>{{ title }}</h5>
</template>

<script>
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'Heading',
  props: {
    title: {
      type: String,
      required: true
    }
  }
})
</script>

<style scoped>
h5 {
  margin-top: 20px;
  margin-bottom: 30px;
}
</style>
