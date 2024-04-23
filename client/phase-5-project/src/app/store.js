import { configureStore } from '@reduxjs/toolkit'
import test_slice_counter from "../features/test_slice_1/test_slice_1"
import test_thunk_slice from "../features/test_slice_2/test_slice_2"
import loggedInUserSlice from '../features/user/userLogged'

export default configureStore({
  reducer: {
    test_counter: test_slice_counter,
    test_thunk: test_thunk_slice,
    loggedInUser: loggedInUserSlice
  },
})

