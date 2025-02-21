import { store } from 'quasar/wrappers'
import { createStore } from 'vuex'

// import example from './module-example'

/*
 * If not building with SSR mode, you can
 * directly export the Store instantiation;
 *
 * The function below can be async too; either use
 * async/await or return a Promise which resolves
 * with the Store instance.
 */

export default store(function (/* { ssrContext } */) {
  const Store = createStore({
    state: {
      isLoggedIn: false,
      operatorsAttandanceRegister: [],
      takenTasks: [],
      tasks: [],
      operator: {},
      activeOperators: [],
      totalTasks: [],
      todayTasks: [],
      activities: [],
      presences: [],
      medications: [],
      incentives: [],
      incentivesLastUpdated: null,
      incentivesCached: false,
      userIncentives: [],
      userIncentivesLastUpdated: null
    },
    mutations: {
      updateLoginStatus(state, status) {
        state.isLoggedIn = status
      },
      updateOperatorRegister(state, status) {
        state.operatorsAttandanceRegister = status
      },
      updateTakenTasks(state, status) {
        state.takenTasks = status
      },
      updateTasks(state, status) {
        state.tasks = status
      },
      updateOperator(state, status) {
        state.operator = status
      },
      updateTotalTasks(state, status) {
        state.totalTasks = status
      },
      addActivity(state, status) {
        state.activities.unshift(status)
      },
      updateChildPresence(state, status) {
        state.presences = status
      },
      updateMedications(state, status) {
        state.medications = status
      },
      updateActiveOperators(state, status) {
        state.activeOperators = status
      },
      updateTodayTasks(state, status) {
        state.todayTasks = status
      },
      setIncentives(state, { data, lastUpdated, cached }) {
        state.incentives = data || []
        state.incentivesLastUpdated = lastUpdated
        state.incentivesCached = cached
      },
      setUserIncentives(state, { data, lastUpdated }) {
        state.userIncentives = data || []
        state.userIncentivesLastUpdated = lastUpdated
      }
    },
    getters: {
      // get the name in the store
      getLoginStatus: state => {
        return state.isLoggedIn
      },
      getOperatorRegister: state => {
        return state.operatorsAttandanceRegister
      },
      getTakenTasks: state => {
        return state.takenTasks
      },
      getTasks: state => {
        return state.tasks
      },
      getOperator: state => {
        return state.operator
      },
      getTotalTasks: state => {
        return state.totalTasks
      },
      getTodayTasks: state => {
        return state.todayTasks
      },
      getActivities: state => {
        return state.activities
      },
      getPresences: state => {
        return state.presences
      },
      getMedications: state => {
        return state.medications
      },
      getActiveOperators: state => {
        return state.activeOperators
      },
      getIncentives: state => {
        return {
          data: state.incentives,
          lastUpdated: state.incentivesLastUpdated,
          cached: state.incentivesCached
        }
      },
      getUserIncentives: state => {
        return {
          data: state.userIncentives,
          lastUpdated: state.userIncentivesLastUpdated
        }
      }
    },
    actions: {
      isTakenTasksEmpty: state => {
        return state.takenTasks === undefined
      },
      isTasksEmpty: state => {
        return state.tasks === undefined
      },
      isTotalTasksEmpty: state => {
        return state.totalTasks === undefined
      }
    },

    // enable strict mode (adds overhead!)
    // for dev mode and --debug builds only
    strict: false //process.env.DEBUGGING
  })

  return Store
})
