import { useSelector } from "react-redux"
import { notificationSelector } from "../../features/user-slice/user"
import NotificationBlock from "./NotificationBlock"
import "../../CSS/notificationlist.css"
import { CardGroup } from "semantic-ui-react"
import 'semantic-ui-css/semantic.min.css'

export default function NotificationList(){

    const userInfo = useSelector((store) => store.user)
    const notifications = useSelector(notificationSelector)

    return(
        <div className="grid-container-noteList">
            <div className="notification-title"><h3>Notifications</h3></div>
            {   Object.keys(userInfo.value).length !== 0 ?
                notifications.map((notification) => {
                    //try to distinguish between friend request notification and post like/ comment like notification
                    return (
                        <CardGroup className="grid-item-noteList">
                            <NotificationBlock key={notification.id} notification={notification}/>
                        </CardGroup>
                )
                })
                :
                null
            }
        </div>
    )
}