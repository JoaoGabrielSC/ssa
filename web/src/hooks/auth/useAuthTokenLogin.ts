import { useCallback } from "react";

// @TODO refactor this to use the API as token matcher
export const useAuthTokenLogin = () => {
    return useCallback((token: string) => {
        localStorage.setItem("token", token);
        window.location.href = "/s/area-config";
    }, [])
}
