
export default function NotificationBlock({notification}){

    //play around with this function and if it works, replace it with redux
    console.log(notification)
    const onResponseChange = (response, e) => {
        console.log(e)
        console.log(response)
        e.preventDefault()
        fetch('/friendships/send_request', {
            method: "PATCH",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                friend_request_response: response,
                friend_request_id: notification.friendship[0].id
            })
        })
        .then((r) => {
            if(r.ok) return r.json()
            else if(r.status === 400) throw new Error(r.json())
            throw new Error(r.json())
        })
        .then((r) => {
            console.log(r)
            window.location.reload()
        })
        .catch((err) => console.log(err))
    }

    return(
        <>
            <span>Notification Dayo!</span>
            <span>{notification.notification_type}</span>
            <p>{notification.text}</p>
            {
                notification.notification_type === "Friend Request"?
                <>
                    <button onClick={(e) => onResponseChange("accepted", e)}>Accept</button>
                    <button onClick={(e) => onResponseChange("rejected", e)}>Reject</button>
                </>
                :
                null
            }
        </>
    )
}