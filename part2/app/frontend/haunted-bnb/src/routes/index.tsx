import { Routes, Route } from 'react-router-dom';
import Places from '../pages/Places';
import Home from '../pages/Home';
import TestLab from '../pages/TestLab';

const Router = () => {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/places" element={<Places />} />
      <Route path="/test-lab" element={<TestLab />} />
    </Routes>
  );
};

export default Router;