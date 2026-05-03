import React, { useState } from 'react';
import { GoogleGenerativeAI } from "@google/generative-ai";
import { motion } from 'framer-motion';

// Aldığın AIza... kodunu buraya yapıştır
const genAI = new GoogleGenerativeAI("AIzaSyCGWNPpkXbkyN5DY9NaqoNV07C6iqSYRUc");
const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });

const App = () => {
  const [cevap, setCevap] = useState("GÜRai Hazır...");

  const konustur = async (soru) => {
    setCevap("Düşünüyorum...");
    const result = await model.generateContent(soru);
    const response = await result.response;
    setCevap(response.text());
  };

  return (
    <div style={{ backgroundColor: 'black', height: '100vh', color: '#00d4ff', textAlign: 'center', paddingTop: '50px' }}>
      {/* O meşhur dönen küren */}
      <motion.div 
        animate={{ rotate: 360 }}
        transition={{ duration: 10, repeat: Infinity, ease: "linear" }}
        style={{ width: '150px', height: '150px', border: '4px dashed #00d4ff', borderRadius: '50%', margin: 'auto', boxShadow: '0 0 30px #00d4ff' }}
      />
      
      <h2 style={{ marginTop: '20px' }}>GÜRai</h2>
      <p style={{ padding: '20px', fontSize: '18px' }}>{cevap}</p>
      
      <button 
        onClick={() => konustur("Merhaba GÜRai, bugün neler yapabiliriz?")}
        style={{ padding: '10px 20px', backgroundColor: '#00d4ff', border: 'none', borderRadius: '5px', cursor: 'pointer' }}
      >
        Jarvis'e Merhaba De!
      </button>
    </div>
  );
};

export default App;
