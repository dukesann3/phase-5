import { configureStore } from '@reduxjs/toolkit'
import test_slice_counter from "../features/test_slice_1/test_slice_1"

export default configureStore({
  reducer: {
    test_counter: test_slice_counter,
  },
})

