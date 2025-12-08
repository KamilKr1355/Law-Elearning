
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { aktywnoscService, contentAdminService } from '../services/api';
import type { QuizQuestion, Odpowiedz } from '../types';
import { Card, Button, Spinner, Badge } from '../components/UI';

export const StudyMode = () => {
  const { kursId } = useParams<{ kursId: string }>();
  const navigate = useNavigate();
  
  const [questions, setQuestions] = useState<QuizQuestion[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isFlipped, setIsFlipped] = useState(false);
  const [loading, setLoading] = useState(true);
  const [correctAnswer, setCorrectAnswer] = useState<string>('');
  const [finished, setFinished] = useState(false);

  useEffect(() => {
    if (kursId) {
      aktywnoscService.getPytaniaNauka(kursId)
        .then(data => {
            if (Array.isArray(data)) {
                setQuestions(data);
            } else {
                setQuestions([]);
            }
        })
        .catch(console.error)
        .finally(() => setLoading(false));
    }
  }, [kursId]);

  useEffect(() => {
    const fetchAnswer = async () => {
        if (!questions[currentIndex]) return;
        
        const q = questions[currentIndex];
        const questionId = q.id || (q as any).pytanie_id;

        if (!questionId) {
            setCorrectAnswer("Błąd danych (brak ID pytania)");
            return;
        }
        
        try {
            const answers: Odpowiedz[] = await contentAdminService.getOdpowiedzi(questionId);
            const correct = answers.find(a => a.poprawna);
            setCorrectAnswer(correct ? correct.tresc : "Brak oznaczonej poprawnej odpowiedzi.");
        } catch (e) {
            console.error(e);
            setCorrectAnswer("Nie udało się pobrać odpowiedzi.");
        }
    };

    if (questions.length > 0 && !finished) {
        fetchAnswer();
    }
  }, [currentIndex, questions, finished]);

  const handleResponse = async (known: boolean) => {
    const currentQ = questions[currentIndex];
    const questionId = currentQ.id || (currentQ as any).pytanie_id;
    
    if (questionId) {
        try {
            await aktywnoscService.updatePostepNauki({
                pytanie_id: questionId,
                is_correct: known
            });
        } catch (e) {
            console.error("Failed to update stats", e);
        }
    }

    if (currentIndex < questions.length - 1) {
        setIsFlipped(false);
        setCurrentIndex(prev => prev + 1);
    } else {
        setFinished(true);
    }
  };

  if (loading) return <Spinner />;
  
  if (questions.length === 0) {
      return (
          <div className="max-w-xl mx-auto text-center mt-20">
              <Card>
                  <h2 className="text-xl font-bold mb-4">Brak materiałów do nauki</h2>
                  <p className="text-gray-500 mb-6">Ten kurs nie posiada jeszcze pytań lub przerobiłeś już cały materiał.</p>
                  <Button onClick={() => navigate(`/kursy/${kursId}`)}>Wróć do kursu</Button>
              </Card>
          </div>
      );
  }

  if (finished) {
      return (
        <div className="max-w-xl mx-auto text-center mt-20">
            <Card className="bg-green-50 border-green-200">
                <div className="text-6xl mb-4">🧠</div>
                <h2 className="text-2xl font-bold text-green-800 mb-4">Sesja zakończona!</h2>
                <p className="text-green-700 mb-6">Przerobiłeś całą dostępną partię materiału.</p>
                <div className="space-x-4">
                    <Button onClick={() => window.location.reload()}>Powtórz</Button>
                    <Button variant="secondary" onClick={() => navigate(`/kursy/${kursId}`)}>Wróć do kursu</Button>
                </div>
            </Card>
        </div>
      );
  }

  const currentQ = questions[currentIndex];
  const progress = ((currentIndex + 1) / questions.length) * 100;

  return (
    <div className="max-w-2xl mx-auto py-6 perspective-1000">
        {/* Progress Bar */}
        <div className="w-full bg-gray-200 rounded-full h-2 mb-6">
            <div className="bg-blue-600 h-2 rounded-full transition-all duration-300" style={{ width: `${progress}%` }}></div>
        </div>

        <div className="flex justify-between items-center mb-6">
            <h1 className="text-2xl font-bold text-gray-800">Tryb Nauki</h1>
            <Badge color="blue">{currentIndex + 1} / {questions.length}</Badge>
        </div>

        {/* Card Container */}
        <div className="relative h-80 w-full cursor-pointer group" onClick={() => setIsFlipped(!isFlipped)}>
            <div className={`relative w-full h-full text-center transition-transform duration-700 transform style-preserve-3d ${isFlipped ? 'rotate-y-180' : ''}`} style={{ transformStyle: 'preserve-3d', transform: isFlipped ? 'rotateY(180deg)' : 'rotateY(0deg)' }}>
                
                {/* Front */}
                <div className="absolute w-full h-full backface-hidden bg-white border-2 border-indigo-100 rounded-2xl shadow-lg flex flex-col items-center justify-center p-8" style={{ backfaceVisibility: 'hidden' }}>
                    <span className="text-xs uppercase text-indigo-500 font-bold mb-4 tracking-wider">Pytanie</span>
                    <h3 className="text-2xl font-medium text-gray-800">{currentQ.tresc}</h3>
                    <p className="text-xs text-gray-400 absolute bottom-4">Kliknij, aby zobaczyć odpowiedź</p>
                </div>

                {/* Back */}
                <div className="absolute w-full h-full backface-hidden bg-indigo-600 rounded-2xl shadow-xl flex flex-col items-center justify-center p-8 text-white" style={{ backfaceVisibility: 'hidden', transform: 'rotateY(180deg)' }}>
                    <span className="text-xs uppercase text-indigo-200 font-bold mb-4 tracking-wider">Poprawna odpowiedź</span>
                    <h3 className="text-2xl font-medium">{correctAnswer || 'Ładowanie odpowiedzi...'}</h3>
                </div>
            </div>
        </div>

        {/* Controls */}
        <div className={`mt-10 flex justify-center space-x-6 transition-opacity duration-300 ${isFlipped ? 'opacity-100' : 'opacity-50 pointer-events-none'}`}>
            <button 
                onClick={(e) => { e.stopPropagation(); handleResponse(false); }}
                className="flex flex-col items-center group"
            >
                <div className="w-14 h-14 rounded-full bg-red-100 text-red-600 flex items-center justify-center text-xl mb-2 group-hover:bg-red-200 group-hover:scale-110 transition-all">✕</div>
                <span className="text-xs font-bold text-gray-500">Jeszcze nie umiem</span>
            </button>

            <button 
                onClick={(e) => { e.stopPropagation(); handleResponse(true); }}
                className="flex flex-col items-center group"
            >
                <div className="w-14 h-14 rounded-full bg-green-100 text-green-600 flex items-center justify-center text-xl mb-2 group-hover:bg-green-200 group-hover:scale-110 transition-all">✓</div>
                <span className="text-xs font-bold text-gray-500">Umiem to!</span>
            </button>
        </div>
    </div>
  );
};
