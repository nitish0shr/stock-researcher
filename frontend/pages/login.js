import Head from 'next/head';

export default function Login() {
  // Placeholder for real login/auth implementation
  return (
    <div>
      <Head><title>Login – Stock Researcher</title></Head>
      <h2>Sign in</h2>
      <form>
        <input type="text" placeholder="Username" />
        <input type="password" placeholder="Password" />
        <button type="submit">Login</button>
      </form>
      <p>Demo login, UI only</p>
    </div>
  );
}
