import 'semantic-ui-css/semantic.min.css'
import { CardContent, CardHeader, CardMeta, CardDescription } from 'semantic-ui-react'
import "../../CSS/friendblock.css"

function FriendBlock({friend}){

    const {first_name, last_name, username, status} = friend

    return(
        <CardContent className="friend-block-content">
            <CardMeta>{status}</CardMeta>
            <div className="friend-block-info-container">
                <CardHeader>USERNAME: {username}</CardHeader>
                <CardDescription>FIRST: {first_name}</CardDescription>
                <CardDescription>LAST: {last_name}</CardDescription>
            </div>
        </CardContent>
    )
}

export default FriendBlock