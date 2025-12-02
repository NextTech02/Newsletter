import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import { CssBaseline, ThemeProvider, createTheme } from '@mui/material'

// Tema customizado com as cores da FCP
const theme = createTheme({
  palette: {
    primary: {
      main: '#FF4B4B',
    },
    secondary: {
      main: '#FFD700',
    },
    tertiary: {
      main: '#4169E1',
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
  },
})

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <App />
    </ThemeProvider>
  </React.StrictMode>,
)
