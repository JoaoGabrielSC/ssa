import { Route } from "wouter";
import { useAuthToken } from "../../hooks/auth/useAuthToken";


export const PrivateRoute = (props: any) => {
  const token = useAuthToken();

  if (!token) {
    window.location.href = "/login"
    return <>NOT PERMITTED</>;
  }

  return <Route {...props} />;
};
