<template>
  <router-view />
</template>
<script>
import { defineComponent } from 'vue'
import IdleJs from 'idle-js'

export default defineComponent({
  name: 'App',
  provide() {
    return {
      resetIdle: this.resetIdle
    }
  },
  data() {
    return {
      idle: null
    }
  },
  mounted() {
    this.idle = new IdleJs({
      idle: 1000 * 60 * 2, // 2 minutes
      events: ['mousemove', 'keydown', 'mousedown', 'touchstart', 'scroll'],
      onIdle: function () {
        const user = JSON.parse(sessionStorage.getItem('user') || '{}')
        if (window.location.pathname === '/login') return
        if (user.usertype !== 'user') return
        sessionStorage.removeItem('access-token')
        window.location.href = '/login'
      }
    })
    this.idle.start()
    return {}
  },
  methods: {
    resetIdle() {
      this.idle.reset()
    }
  }
})
</script>

<style>
body {
  overflow-y: auto;
}
</style>
