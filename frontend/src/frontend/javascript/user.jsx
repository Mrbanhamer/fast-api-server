const UserDashboard = () => {
    const [user, setUser] = React.useState(null);
    const [error, setError] = React.useState(null);

    React.useEffect(() => {
        // This runs as soon as the page loads
        fetch('/user/me')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Not logged in');
                }
                return response.json();
            })
            .then(data => setUser(data))
            .catch(err => {
                setError(err.message);
                // Optional: Redirect to login if unauthorized
                // window.location.href = "/user/login";
            });
    }, []);

    if (error) return <div className="error">Error: {error}. Please log in.</div>;
    if (!user) return <div>Loading profile...</div>;

    return (
        <div className="dashboard-container">
            <h1>Welcome, {user.username}!</h1>
            <div className="profile-card">
                <p><strong>Email:</strong> {user.email}</p>
                <p><strong>User ID:</strong> {user.id}</p>
            </div>
            <button onClick={() => window.location.href = "/user/logout"}>
                Log Out
            </button>
        </div>
    );
};

// Make it available for App()
window.UserDashboard = UserDashboard;