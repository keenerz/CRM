import React, { useContext, useState, useEffect } from "react";
import { Context } from "../store/appContext";
import { useHistory, Link } from "react-router-dom";
import "../../styles/accountcreation.css";

export const AccountCreation = () => {
  const { store, actions } = useContext(Context);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [passwordRepeat, setPasswordRepeat] = useState("");
  const history = useHistory();

  let matchingPassword = () => {
    if (password !== passwordRepeat) {
      return false;
    } else {
      return true;
    }
  };

  return (
    <section className="register1">
      <div className="form-container">
        <div className="image-holder"></div>
        <div className="form">
          <form
            method="post"
            onSubmit={(e) => {
              if (matchingPassword() === false) {
                alert("Make sure your passwords are matching!");
                e.preventDefault();
              } else {
                actions
                  .createUser(email, password, username)
                  .then((session) => history.push("/login"));
                e.preventDefault();
              }
            }}
          >
            <h2 className="text-center">
              <strong>Create</strong> an account.
            </h2>
            <div className="mb-3">
              <label for="email" className="form-label">
                Email
              </label>
              <input
                className="form-control border"
                type="email"
                name="email"
                placeholder="user@user.com"
                id="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
            <div className="mb-3">
              <label for="password" className="form-label">
                Password
              </label>
              <input
                className="form-control border"
                type="password"
                name="password"
                placeholder="Password"
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
            <div className="mb-3">
              <label for="password-repeat" className="form-label">
                Password Confirmation
              </label>
              <input
                className="form-control border"
                type="password"
                name="password-repeat"
                placeholder="Password (Repeat)"
                id="password-repeat"
                value={passwordRepeat}
                onChange={(e) => {
                  setPasswordRepeat(e.target.value);
                  matchingPassword();
                }}
              />
            </div>
            {matchingPassword() === false ? (
              <div className="alert alert-danger" role="alert">
                Passwords do not match!
              </div>
            ) : null}

            <div className="mb-3">
              <Link to="/accountcreation" className="already">
                <button className="btn btn-primary d-block w-100" type="submit">
                  Sign Up
                </button>
              </Link>
            </div>
            <Link to="/" className="already">
              You already have an account? Login.
            </Link>
          </form>
        </div>
      </div>
    </section>
  );
};
