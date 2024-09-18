import { useState } from "react";
import { useAuthTokenLogin } from "../../hooks/auth/useAuthTokenLogin"

export const LoginPage = () => {
    const login = useAuthTokenLogin();
    const [token, setToken] = useState<string>();

    return (
        <div>
            <h1>Login</h1>
            <input type="text" placeholder="username" onChange={(evt) => setToken(evt.target.value)} />
            <button onClick={() => token && login(token)}>Login</button>
        </div>
    )
}
