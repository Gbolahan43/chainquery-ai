import { useState, useCallback } from 'react';
import { Outlet } from 'react-router-dom';
import { Sidebar } from './Sidebar';
import { Navbar } from './Navbar';

export interface LayoutContext {
  selectedSQL: string;
  selectedInput: string;
  setSelectedQuery: (sql: string, input: string) => void;
}

export function Layout() {
  const [collapsed, setCollapsed] = useState(false);
  const [selectedSQL, setSelectedSQL] = useState('');
  const [selectedInput, setSelectedInput] = useState('');

  const handleSelectQuery = useCallback((sql: string, input: string) => {
    setSelectedSQL(sql);
    setSelectedInput(input);
  }, []);

  return (
    <div className="flex h-screen w-full overflow-hidden bg-background">
      <Sidebar
        onSelectQuery={handleSelectQuery}
        collapsed={collapsed}
        onToggle={() => setCollapsed(!collapsed)}
      />
      
      <main className="flex-1 flex flex-col overflow-hidden">
        <Navbar />
        <div className="flex-1 overflow-auto">
          <Outlet context={{ selectedSQL, selectedInput, setSelectedQuery: handleSelectQuery }} />
        </div>
      </main>
    </div>
  );
}
