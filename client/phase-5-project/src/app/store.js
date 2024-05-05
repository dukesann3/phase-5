import { configureStore } from '@reduxjs/toolkit'

import userSlice from '../features/user-slice/user'
import postSlice from '../features/post-slice/allPosts'
import userListSlice from '../features/user-slice/userList'

export default configureStore({
  reducer: {
    user: userSlice,
    allPost: postSlice,
    userList: userListSlice
  },
})

