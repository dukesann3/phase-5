import { useDispatch, useSelector } from "react-redux"
import { getFriends, unfriend } from "../../features/friend-slice/friend"
import { useEffect } from "react"
import { getPosts } from "../../features/post-slice/allPosts"
import { NavLink } from "react-router-dom"
import FriendBlock from "./FriendBlock"
import 'semantic-ui-css/semantic.min.css'
import { CardGroup, Card, Button } from "semantic-ui-react"
import "../../CSS/friendslist.css"

function FriendsList(){

    const dispatch = useDispatch()
    const friends = useSelector((state) => state.friends)

    useEffect(() => {
        dispatch(getFriends())
        dispatch(getPosts())
    },[])

    return(
        <div className="friends-list-container">
            <div className="friends-list-word-container">
                <span>Friends List</span>
            </div>
            {
                Object.keys(friends.value).length !== 0 ?

                <CardGroup itemsPerRow={5}>
                    {friends.value.map((f) => {
                        return (
                            <Card>
                                <NavLink to={`/user/${f.id}/profile`}>
                                    <FriendBlock key={f.id} friend={f} status={f.status}/>
                                </NavLink>
                                {f.status !== "pending" ? <Button onClick={() => dispatch(unfriend(f.id))}>unfriend</Button> : null}
                            </Card>
                        )
                    })}
                </CardGroup>

                :
                null
            }
        </div>
    )
}

export default FriendsList