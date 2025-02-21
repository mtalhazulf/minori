<template>
  <table>
    <thead>
      <tr>
        <th class="top-left"></th>
        <th>Lunedì</th>
        <th>Martedì</th>
        <th>Mercoledì</th>
        <th>Giovedì</th>
        <th>Venerdì</th>
        <th>Sabato</th>
        <th>Domenica</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <th>Mattina</th>
        <td v-for="day in Object.values(dayofweek)" :key="(day, Mattina)">
          <q-checkbox v-model="periods" size="lg" :val="`${day}-Mattina`" />
        </td>
      </tr>
      <tr>
        <th>Pomeriggio</th>
        <td v-for="day in Object.values(dayofweek)" :key="(day, Pomeriggio)">
          <q-checkbox v-model="periods" size="lg" :val="`${day}-Pomeriggio`" />
        </td>
      </tr>
      <tr>
        <th>Sera</th>
        <td v-for="day in Object.values(dayofweek)" :key="(day, Sera)">
          <q-checkbox v-model="periods" size="lg" :val="`${day}-Sera`" />
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script>
import { ref } from 'vue'
export default {
  name: 'WeeklyCheckboxCalendar',

  props: {
    dayofweek: {
      type: Object,
      required: true
    }
  },
  emits: ['periods'],

  data() {
    return {
      periods: ref([])
    }
  },
  watch: {
    periods: function (newVal) {
      this.$emit('periods', newVal)
    }
  }
}
</script>

<style scoped>
table {
  margin: 0 auto;
  border-collapse: collapse;
  font-family: Arial, sans-serif;
  font-size: 14px;
}

th,
td {
  padding: 8px;
  text-align: center;
  border: 1px solid #ddd;
}

th {
  background-color: #a0d1ff88;
}
</style>
