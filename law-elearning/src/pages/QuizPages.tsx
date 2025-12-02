import React, { useState, useEffect } from 'react';
import { useNavigate, useParams, useSearchParams, useLocation } from 'react-router-dom';
import { quizService, kursService } from '../services/api';
import type { QuizQuestion, Kurs } from '../types';
import { Card, Button, Spinner, Badge } from '../components/UI';

export const QuizStart = () => {
  const [kursy, setKursy] = useState<Kurs[]>([]);
  const [selectedKurs, setSelectedKurs] = useState<string>('');
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    kursService.getAll().then(setKursy).finally(() => setLoading(false));
  }, []);

  const handleStart = () => {
    if (selectedKurs) {
      const kursName = kursy.find(k => k.id.toString() === selectedKurs)?.nazwa_kursu;
      if (kursName) {
        navigate(`/quiz/play?kurs=${encodeURIComponent(kursName)}&id=${selectedKurs}`);
      }
    }
  };

  if (loading) return <Spinner />;

  return (
    <div className="max-w-2xl mx-auto py-10">
      <Card className="text-center p-10">
        <h1 className="text-3xl font-bold text-indigo-900 mb-6">Sprawdź swoją wiedzę</h1>
        <p className="text-gray-600 mb-8">Wybierz kurs, z którego chcesz przeprowadzić egzamin próbny.</p>
        
        <div className="max-w-xs mx-auto mb-8">
          <label className="block text-left text-sm font-bold mb-2 text-gray-700">Wybierz kurs</label>
          <select 
            className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none bg-white"
            value={selectedKurs}
            onChange={(e) => setSelectedKurs(e.target.value)}
          >
            <option value="">-- Wybierz --</option>
            {kursy.map(k => (
              <option key={k.id} value={k.id}>{k.nazwa_kursu}</option>
            ))}
          </select>
        </div>

        <Button 
          onClick={handleStart} 
          disabled={!selectedKurs} 
          className={`w-full py-4 text-lg ${!selectedKurs ? 'opacity-50 cursor-not-allowed' : ''}`}
        >
          Rozpocznij Quiz 🚀
        </Button>
      </Card>
    </div>
  );
};

export const QuizActive = () => {
  const [searchParams] = useSearchParams();
  const kursNazwa = searchParams.get('kurs');
  const kursId = searchParams.get('id');
  const navigate = useNavigate();

  const [questions, setQuestions] = useState<QuizQuestion[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState<{ [key: number]: number }>({}); // questionId -> answerId
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    if (kursNazwa) {
      quizService.start(kursNazwa)
        .then(setQuestions)
        .catch(err => alert('Nie udało się pobrać pytań. Upewnij się, że kurs ma pytania.'))
        .finally(() => setLoading(false));
    }
  }, [kursNazwa]);

  const handleSelect = (questionId: number, answerId: number) => {
    setAnswers(prev => ({ ...prev, [questionId]: answerId }));
  };

  const handleNext = () => {
    if (currentIndex < questions.length - 1) {
      setCurrentIndex(prev => prev + 1);
    }
  };

  const handlePrev = () => {
    if (currentIndex > 0) {
      setCurrentIndex(prev => prev - 1);
    }
  };

  const handleFinish = async () => {
    if (!kursId) return;
    setSubmitting(true);
    
    const formattedAnswers = Object.entries(answers).map(([qid, aid]) => ({
      pytanie_id: parseInt(qid),
      wybrana_opcja: aid
    }));

    try {
      const result = await quizService.check({
        kurs_id: parseInt(kursId),
        odpowiedzi: formattedAnswers
      });
      // Pass result to summary page via state
      navigate('/quiz/wynik', { state: { result, total: questions.length, kursId } });
    } catch (e) {
      console.error(e);
      alert('Błąd podczas wysyłania odpowiedzi.');
      setSubmitting(false);
    }
  };

  if (loading) return <Spinner />;
  if (questions.length === 0) return <div className="text-center p-10">Brak pytań dla tego kursu. <Button onClick={() => navigate('/quiz')} variant="secondary" className="ml-4">Wróć</Button></div>;

  const currentQ = questions[currentIndex];
  const progress = ((currentIndex + 1) / questions.length) * 100;
  const isAnswered = answers[currentQ.id] !== undefined;
  const isLast = currentIndex === questions.length - 1;
  const allAnswered = questions.every(q => answers[q.id] !== undefined);

  return (
    <div className="max-w-3xl mx-auto py-6">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-xl font-bold text-gray-700">Pytanie {currentIndex + 1} / {questions.length}</h2>
        <Badge>{kursNazwa}</Badge>
      </div>
      
      {/* Progress Bar */}
      <div className="w-full bg-gray-200 rounded-full h-2 mb-8">
        <div className="bg-indigo-600 h-2 rounded-full transition-all duration-300" style={{ width: `${progress}%` }}></div>
      </div>

      <Card className="min-h-[300px] flex flex-col justify-center">
        <h3 className="text-2xl font-medium text-gray-900 mb-8">{currentQ.tresc}</h3>
        <div className="space-y-3">
          {currentQ.odpowiedzi.map((odp) => (
            <div 
              key={odp.id}
              onClick={() => handleSelect(currentQ.id, odp.id)}
              className={`p-4 rounded-lg border cursor-pointer transition-all flex items-center ${
                answers[currentQ.id] === odp.id 
                  ? 'border-indigo-600 bg-indigo-50 ring-1 ring-indigo-600' 
                  : 'border-gray-200 hover:bg-gray-50'
              }`}
            >
              <div className={`w-5 h-5 rounded-full border mr-4 flex items-center justify-center ${
                answers[currentQ.id] === odp.id ? 'border-indigo-600' : 'border-gray-400'
              }`}>
                {answers[currentQ.id] === odp.id && <div className="w-3 h-3 bg-indigo-600 rounded-full"></div>}
              </div>
              <span className="text-gray-800">{odp.tresc}</span>
            </div>
          ))}
        </div>
      </Card>

      <div className="flex justify-between mt-8">
        <Button onClick={handlePrev} disabled={currentIndex === 0} variant="secondary">Poprzednie</Button>
        
        {isLast ? (
          <Button onClick={handleFinish} disabled={!allAnswered || submitting} variant="primary" className="bg-green-600 hover:bg-green-700">
             {submitting ? 'Sprawdzanie...' : 'Zakończ Quiz'}
          </Button>
        ) : (
          <Button onClick={handleNext} disabled={!isAnswered}>Następne</Button>
        )}
      </div>
    </div>
  );
};

export const QuizSummary = () => {
  const navigate = useNavigate();
  // Retrieve state passed from navigation
  const { state: locState } = useLocation();

  if (!locState || !locState.result) {
    return <div className="text-center mt-10">Brak wyników. <Button onClick={() => navigate('/quiz')}>Wróć</Button></div>;
  }

  const { result, total, kursId } = locState;
  const percentage = Math.round(result.wynik);

  return (
    <div className="max-w-xl mx-auto py-10 text-center">
      <Card>
        <div className="mb-6">
          {percentage >= 50 ? (
            <div className="text-6xl mb-4">🎉</div>
          ) : (
            <div className="text-6xl mb-4">📚</div>
          )}
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            {percentage >= 50 ? 'Gratulacje! Zdałeś.' : 'Niestety, musisz jeszcze poćwiczyć.'}
          </h1>
          <p className="text-gray-500">Twój wynik egzaminu</p>
        </div>

        <div className="flex justify-center items-center mb-8">
          <div className={`w-32 h-32 rounded-full flex items-center justify-center text-3xl font-bold border-8 ${
            percentage >= 50 ? 'border-green-500 text-green-600' : 'border-red-500 text-red-600'
          }`}>
            {percentage}%
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4 mb-8 bg-gray-50 p-4 rounded-xl">
          <div className="text-center">
            <p className="text-xs text-gray-500 uppercase font-bold">Punkty</p>
            <p className="text-xl font-bold text-gray-800">{result.punkty} / {total}</p>
          </div>
          <div className="text-center">
            <p className="text-xs text-gray-500 uppercase font-bold">Poprawne</p>
            <p className="text-xl font-bold text-gray-800">{result.poprawne.length}</p>
          </div>
        </div>

        <div className="space-y-3">
          <Button className="w-full" onClick={() => navigate(`/quiz`)}>Rozwiąż kolejny Quiz</Button>
          <Button variant="secondary" className="w-full" onClick={() => navigate(`/kursy/${kursId}`)}>Wróć do Kursu</Button>
        </div>
      </Card>
    </div>
  );
};