import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

function ErrorPage(){

    const navigate = useNavigate()
    useEffect(()=>{
        setTimeout(() => {
            navigate(-1)
        }, 3000)
    },[])

    return(
        <>
            <h1>Error Page</h1>
            <h3>Page Not Found</h3>
        </>
    )
}

export default ErrorPage;