import {http, HttpResponse} from 'msw'

export const handlers = [
    http.get('/checksession', () => {
        return HttpResponse.json({
            first_name: "a",
            last_name: "a",
            username: "a",
        })
    })
]
