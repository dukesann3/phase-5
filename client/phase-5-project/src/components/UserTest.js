import { useState } from "react"

export default function UserTest(){

    const [form, setForm] = useState({
        image_src: ""
    })

    async function newUserPost(){

        console.log(form)

        if(form.image_src === ""){
            return
        }

        await fetch("/testing", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(form)
        }).then((r) => {
            if(r.ok) return r.json()
            throw new Error("Test Error")
        }).then(r => console.log(r))
        .catch((error) => console.log(error))
    }
    
    function handleFormChange(e){
        const reader = new FileReader()
        reader.readAsDataURL(e.target.files[0])

        reader.addEventListener("load", () => {
            const url = reader.result
            setForm({
                image_src: url
            })
        })
    }

    return(
        <div className="test">
            <h1>This is a test</h1>
            <form onSubmit={() => newUserPost()}>
                <input 
                type="file" 
                id="image_src"
                onChange={handleFormChange}
                />
                <input 
                type="submit"
                />
            </form>
        </div>
    )
}
