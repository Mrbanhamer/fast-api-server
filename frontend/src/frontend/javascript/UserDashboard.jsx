function UserDashboard() {
    const [user, setUser] = React.useState(null);
    const [tasks, setTasks] = React.useState([]);
    const [taskTitle, setTaskTitle] = React.useState("");

    // --- Fetch Data ---
    const loadAllData = async () => {
        try {
            // Get User Profile
            const userRes = await fetch('/user/me', { credentials: 'include' });
            if (!userRes.ok) throw new Error("Unauthorized");
            const userData = await userRes.json();
            setUser(userData);

            // Get User Tasks
            const taskRes = await fetch('/tasks/', { credentials: 'include' });
            const taskData = await taskRes.json();
            setTasks(Array.isArray(taskData) ? taskData : []);
        } catch (err) {
            console.error("Session expired or invalid:", err);
            window.location.href = "/user/login";
        }
    };

    React.useEffect(() => {
        loadAllData();
    }, []);

    // --- Actions ---
    const handleAddTask = async (e) => {
        e.preventDefault();
        if (!taskTitle.trim()) return;

        const response = await fetch('/tasks/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                title: taskTitle, 
                description: "New task from dashboard", 
                completed: false 
            }),
            credentials: 'include'
        });

        if (response.ok) {
            setTaskTitle("");
            loadAllData(); // Refresh list
        }
    };

    const handleDeleteTask = async (taskId) => {
        const response = await fetch(`/tasks/${taskId}`, {
            method: 'DELETE',
            credentials: 'include'
        });

        if (response.ok) {
            // Instant UI update
            setTasks(prev => prev.filter(t => t.id !== taskId));
        }
    };

    const handleToggleComplete = async (task) => {
    await fetch(`/tasks/${task.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
            title: task.title, 
            description: task.description, 
            completed: !task.completed // Switch the status
        }),
        credentials: 'include'
    });
    loadAllData(); // Refresh the list
    };

    if (!user) return <div style={{ padding: '20px' }}>Loading...</div>;

    return (
        <div style={{ maxWidth: '600px', margin: '40px auto', fontFamily: 'Arial, sans-serif' }}>
            <header style={{ borderBottom: '2px solid #eee', paddingBottom: '10px', marginBottom: '20px' }}>
                <h2>Welcome, {user.name} {user.last_name}</h2>
                <p style={{ color: '#666' }}>{user.email}</p>
            </header>

            {/* Add Task Form */}
            <form onSubmit={handleAddTask} style={{ display: 'flex', gap: '10px', marginBottom: '30px' }}>
                <input 
                    type="text"
                    placeholder="Enter a new task..."
                    value={taskTitle}
                    onChange={(e) => setTaskTitle(e.target.value)}
                    style={{ flex: 1, padding: '10px', borderRadius: '4px', border: '1px solid #ccc' }}
                />
                <button type="submit" style={{ padding: '10px 20px', backgroundColor: '#28a745', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
                    Add Task
                </button>
            </form>

            {/* Task List */}
            <div style={{ background: '#f9f9f9', borderRadius: '8px', padding: '10px' }}>
                <h3>Your Tasks</h3>
                {tasks.length === 0 ? <p>No tasks yet. Add one above!</p> : (
                    <ul style={{ listStyle: 'none', padding: 0 }}>
                        {tasks.map(task => (
                            <li key={task.id} style={{ 
                                background: 'white', 
                                margin: '10px 0', 
                                padding: '15px', 
                                borderRadius: '5px', 
                                display: 'flex', 
                                justifyContent: 'space-between',
                                alignItems: 'center',
                                boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
                            }}>
                                <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                                    <input 
                                        type="checkbox" 
                                        checked={task.completed} 
                                        onChange={() => handleToggleComplete(task)} 
                                        style={{ cursor: 'pointer' }}
                                    />
                                    <span style={{ textDecoration: task.completed ? 'line-through' : 'none' }}>
                                        {task.title}
                                    </span>
                                </div>
                                <button 
                                    onClick={() => handleDeleteTask(task.id)}
                                    style={{ backgroundColor: '#dc3545', color: 'white', border: 'none', padding: '5px 10px', borderRadius: '3px', cursor: 'pointer' }}
                                >
                                    Delete
                                </button>
                            </li>
                        ))}
                    </ul>
                )}
            </div>
        </div>
    );
}