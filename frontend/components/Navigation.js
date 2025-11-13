import Link from 'next/link'
import { useRouter } from 'next/router'

export default function Navigation() {
  const router = useRouter()

  const isActive = (pathname) => {
    return router.pathname === pathname
  }

  return (
    <nav style={styles.nav}>
      <div style={styles.container}>
        <Link href="/" style={styles.logo}>
          📊 Stock Researcher
        </Link>
        
        <div style={styles.links}>
          <Link 
            href="/" 
            style={{...styles.link, ...(isActive('/') && styles.activeLink)}}
          >
            Dashboard
          </Link>
          <Link 
            href="/stocks" 
            style={{...styles.link, ...(isActive('/stocks') && styles.activeLink)}}
          >
            Stocks
          </Link>
          <Link 
            href="/analysis" 
            style={{...styles.link, ...(isActive('/analysis') && styles.activeLink)}}
          >
            Analysis
          </Link>
          <Link 
            href="/login" 
            style={{...styles.link, ...(isActive('/login') && styles.activeLink)}}
          >
            Login
          </Link>
        </div>
      </div>
    </nav>
  )
}

const styles = {
  nav: {
    background: '#1a1a1a',
    borderBottom: '1px solid #333',
    padding: '1rem 0',
  },
  container: {
    maxWidth: '1200px',
    margin: '0 auto',
    padding: '0 20px',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  logo: {
    fontSize: '1.5rem',
    fontWeight: 'bold',
    color: '#fff',
    textDecoration: 'none',
  },
  links: {
    display: 'flex',
    gap: '2rem',
  },
  link: {
    color: '#999',
    textDecoration: 'none',
    transition: 'color 0.2s',
  },
  activeLink: {
    color: '#4a90e2',
    fontWeight: 'bold',
  },
}
