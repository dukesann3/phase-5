import {render, screen} from '@testing-library/react'
import '@testing-library/jest-dom'
import { Provider } from 'react-redux'
import * as React from "react"
import store from '../app/store'
import { RouterProvider, createMemoryRouter } from 'react-router-dom'
import routes from '../routes'
import { server } from '../mocks/node'

server.listen()

const router = createMemoryRouter(routes, {
    initialEntries: ["/"],
})

test('load test', async () => {
    render(
        <Provider store={store}>
            <RouterProvider router={router}/>
        </Provider>
    )
    screen.debug()
}) 

test('fetch-msw', () => {
    fetch('/checksession')
})
