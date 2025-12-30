import React, { useState, useEffect } from 'react';
import { useNavigate, useSearchParams, useLocation, Link } from 'react-router-dom';
import { quizService, kursService, aktywnoscService } from '../services/api';
import type { QuizQuestion, Kurs, Rozdzial, QuizResult, Odpowiedz } from '../types';
import { Card, Button, Spinner, Badge } from '../components/UI';

export const QuizStart = () => {
  const [kursy, setKursy] = useState<Kurs[]>([]);
  const [selectedKurs, setSelectedKurs] = useState<string>('');
  const [rozdzialy, setRozdzialy] = useState<Rozdzial[]>([]);
  const [selectedRozdzialy, setSelectedRozdzialy] = useState<number[]>([]);
  const [loading, setLoading] = useState(true);
  const [loadingRozdzialy, setLoadingRozdzialy] = useState(false);
  const navigate = useNavigate();
  const [params] = useSearchParams();
  const initialKursId = params.get('kursId');

  useEffect(() => {
    kursService.getAll().then(data => {
        const list = Array.isArray(data) ? data : [];
        setKursy(list);
        if (initialKursId) {
            setSelectedKurs(initialKursId);
        }
    }).finally(() => setLoading(false));
  }, [initialKursId]);

  useEffect(() => {
      if (selectedKurs) {
          setLoadingRozdzialy(true);
          setRozdzialy([]);
          setSelectedRozdzialy([]);

          kursService.getRozdzialy(selectedKurs)
            .then(data => {
                const safeData = Array.isArray(data) ? data : [];
                setRozdzialy(safeData);
                // Domyślnie zaznaczamy wszystkie rozdziały
                setSelectedRozdzialy(safeData.map((r: any) => r.id));
            })
            .catch(err => {
                console.warn("Nie znaleziono rozdziałów dla tego kursu", err);
                setRozdzialy([]);
                setSelectedRozdzialy([]);
            })
            .finally(() => setLoadingRozdzialy(false));
      } else {
          setRozdzialy([]);
          setSelectedRozdzialy([]);
      }
  }, [selectedKurs]);

  const handleToggleRozdzial = (id: number) => {
      setSelectedRozdzialy(prev => 
          prev.includes(id) ? prev.filter(rid => rid !== id) : [...prev, id]
      );
  };

  const handleStart = () => {
    if (selectedKurs) {
      const currentKurs = kursy.find(k => k.id.toString() === selectedKurs);
      const kursName = currentKurs?.nazwa_kursu;
      if (kursName) {
        const isAllSelected = selectedRozdzialy.length === rozdzialy.length;
        const rozdzialyQuery = (isAllSelected || rozdzialy.length === 0) ? '' : selectedRozdzialy.join(',');
        navigate(`/quiz/play?kurs=${encodeURIComponent(kursName)}&id=${selectedKurs}${rozdzialyQuery ? `&rozdzialy=${rozdzialyQuery}` : ''}`);
      }
    }
  };

  if (loading) return <Spinner />;

  return (
    <div className="max-w-2xl mx-auto py-10">
      <Card className="p-10">
        <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-indigo-900 mb-4">Sprawdź swoją wiedzę</h1>
            <p className="text-gray-600">Skonfiguruj zakres egzaminu próbnego.</p>
        </div>
        
        <div className="space-y-6">
            {!initialKursId ? (
                <div className="max-w-xs mx-auto">
                    <label className="block text-left text-sm font-bold mb-2 text-gray-700">1. Wybierz kurs</label>
                    <select 
                        className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none bg-white"
                        value={selectedKurs}
                        onChange={(e) => setSelectedKurs(e.target.value)}
                    >
                        <option value="">-- Wybierz kurs --</option>
                        {kursy.map(k => (
                        <option key={k.id} value={k.id}>{k.nazwa_kursu}</option>
                        ))}
                    </select>
                </div>
            ) : (
                <div className="text-center bg-indigo-50 p-3 rounded-lg border border-indigo-100 mb-4">
                    <span className="text-xs uppercase text-indigo-400 font-bold block mb-1">Kurs wybrany</span>
                    <span className="font-bold text-indigo-900">{kursy.find(k => k.id.toString() === selectedKurs)?.nazwa_kursu}</span>
                </div>
            )}

            {selectedKurs && (
                <div className="animate-fadeIn">
                    <label className="block text-sm font-bold mb-3 text-gray-700">
                        {initialKursId ? 'Wybierz zakres materiału' : '2. Wybierz zakres materiału'}
                    </label>
                    {loadingRozdzialy ? <Spinner /> : (
                        <div className="bg-gray-50 p-4 rounded-xl border border-gray-100 grid grid-cols-1 gap-2 max-h-60 overflow-y-auto">
                            {rozdzialy.length === 0 ? (
                                <div className="text-center py-4">
                                    <p className="text-gray-400 text-sm italic">Ten kurs nie posiada jeszcze zdefiniowanych rozdziałów.</p>
                                    <p className="text-xs text-indigo-500 mt-1">Egzamin obejmie wszystkie dostępne pytania kursu.</p>
                                </div>
                            ) : (
                                rozdzialy.map(r => (
                                    <label key={r.id} className="flex items-center space-x-3 p-2 hover:bg-white rounded-lg transition-colors cursor-pointer group">
                                        <input 
                                            type="checkbox" 
                                            checked={selectedRozdzialy.includes(r.id)}
                                            onChange={() => handleToggleRozdzial(r.id)}
                                            className="w-5 h-5 text-indigo-600 rounded focus:ring-indigo-500 cursor-pointer"
                                        />
                                        <span className={`text-sm ${selectedRozdzialy.includes(r.id) ? 'text-gray-900 font-medium' : 'text-gray-500'}`}>
                                            {r.nazwa_rozdzialu}
                                        </span>
                                    </label>
                                ))
                            )}
                        </div>
                    )}
                    
                    {rozdzialy.length > 0 && !loadingRozdzialy && (
                        <div className="flex justify-between mt-2 px-1">
                            <button 
                                onClick={() => setSelectedRozdzialy(rozdzialy.map(r => r.id))}
                                className="text-xs text-indigo-600 hover:underline"
                            >Zaznacz wszystkie</button>
                            <button 
                                onClick={() => setSelectedRozdzialy([])}
                                className="text-xs text-gray-500 hover:underline"
                            >Odznacz wszystkie</button>
                        </div>
                    )}
                </div>
            )}
        </div>

        <Button 
          onClick={handleStart} 
          disabled={!selectedKurs || (rozdzialy.length > 0 && selectedRozdzialy.length === 0)} 
          className={`w-full mt-10 py-4 text-lg shadow-indigo-100 ${(!selectedKurs || (rozdzialy.length > 0 && selectedRozdzialy.length === 0)) ? 'opacity-50 cursor-not-allowed' : ''}`}
        >
          Rozpocznij Quiz 🚀
        </Button>
        
        {initialKursId && (
            <Link to="/quiz" className="block text-center mt-4 text-xs text-gray-400 hover:text-indigo-500 underline transition">
                Zmień kurs
            </Link>
        )}
      </Card>
    </div>
  );
};

export const QuizActive = () => {
  const [searchParams] = useSearchParams();
  const kursNazwa = searchParams.get('kurs');
  const kursId = searchParams.get('id');
  const rozdzialy = searchParams.get('rozdzialy');
  const navigate = useNavigate();

  const [questions, setQuestions] = useState<QuizQuestion[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState<{ [key: number]: number }>({}); // questionId -> answerId
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    if (kursNazwa) {
      quizService.start(kursNazwa, rozdzialy || undefined)
        .then(setQuestions)
        .catch(err => {
            console.error(err);
            alert('Nie udało się pobrać pytań. Spróbuj zmienić zakres materiału.');
            navigate('/quiz');
        })
        .finally(() => setLoading(false));
    }
  }, [kursNazwa, rozdzialy, navigate]);

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
      wybrana_opcja: aid as number
    }));

    try {
      const result = await quizService.check({
        kurs_id: parseInt(kursId),
        odpowiedzi: formattedAnswers
      });

      // AKTUALIZACJA STATUSÓW PYTAŃ (OP / OZ)
      try {
          await Promise.all(formattedAnswers.map(ans => {
              const isCorrect = result.poprawne.includes(ans.pytanie_id);
              return aktywnoscService.updateStatusPytania(ans.pytanie_id, isCorrect ? 'OP' : 'OZ');
          }));
      } catch (statusError) {
          console.warn("Błąd podczas aktualizacji statusów pytań", statusError);
      }

      // Przekazujemy listę pytań do raportu review
      navigate('/quiz/wynik', { state: { result, total: questions.length, kursId, questions } });
    } catch (e) {
      console.error(e);
      alert('Błąd podczas wysyłania odpowiedzi.');
      setSubmitting(false);
    }
  };

  if (loading) return <Spinner />;
  if (questions.length === 0) return (
    <div className="text-center p-10">
        <h2 className="text-xl font-bold mb-4">Brak pytań spełniających kryteria.</h2>
        <Button onClick={() => navigate('/quiz')} variant="secondary">Wróć i zmień zakres</Button>
    </div>
  );

  const currentQ = questions[currentIndex];
  const progress = ((currentIndex + 1) / questions.length) * 100;
  const isAnswered = answers[currentQ.id] !== undefined;
  const isLast = currentIndex === questions.length - 1;
  const allAnswered = questions.every(q => answers[q.id] !== undefined);

  return (
    <div className="max-w-3xl mx-auto py-6">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-xl font-bold text-gray-700">Pytanie {currentIndex + 1} / {questions.length}</h2>
        <Badge color="blue" className="bg-indigo-100 text-indigo-700">{kursNazwa}</Badge>
      </div>
      
      <div className="w-full bg-gray-200 rounded-full h-2 mb-8">
        <div className="bg-indigo-600 h-2 rounded-full transition-all duration-300" style={{ width: `${progress}%` }}></div>
      </div>

      <Card className="min-h-[300px] flex flex-col justify-center border-indigo-50 shadow-md">
        <h3 className="text-2xl font-medium text-gray-900 mb-8 leading-tight">{currentQ.tresc}</h3>
        <div className="space-y-3">
          {currentQ.odpowiedzi.map((odp) => (
            <div 
              key={odp.id}
              onClick={() => handleSelect(currentQ.id, odp.id)}
              className={`p-4 rounded-lg border cursor-pointer transition-all flex items-center ${
                answers[currentQ.id] === odp.id 
                  ? 'border-indigo-600 bg-indigo-50 ring-2 ring-indigo-600' 
                  : 'border-gray-200 hover:border-indigo-300 hover:bg-gray-50'
              }`}
            >
              <div className={`w-5 h-5 rounded-full border mr-4 flex items-center justify-center ${
                answers[currentQ.id] === odp.id ? 'border-indigo-600' : 'border-gray-400'
              }`}>
                {answers[currentQ.id] === odp.id && <div className="w-3 h-3 bg-indigo-600 rounded-full"></div>}
              </div>
              <span className="text-gray-800 font-medium">{odp.tresc}</span>
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
  const { state: locState } = useLocation();

  if (!locState || !locState.result) {
    return <div className="text-center mt-10">Brak wyników. <Button onClick={() => navigate('/quiz')}>Wróć</Button></div>;
  }

  const { result, total, kursId, questions } = locState as { result: QuizResult, total: number, kursId: string, questions: QuizQuestion[] };
  const percentage = Math.round(result.wynik);

  return (
    <div className="max-w-4xl mx-auto py-10 space-y-10">
      <Card className="text-center p-10 shadow-xl border-indigo-50">
        <div className="mb-6">
          {percentage >= 50 ? (
            <div className="text-6xl mb-4 animate-bounce">🎉</div>
          ) : (
            <div className="text-6xl mb-4">📚</div>
          )}
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            {percentage >= 50 ? 'Gratulacje! Zdałeś.' : 'Niestety, musisz jeszcze poćwiczyć.'}
          </h1>
          <p className="text-gray-500 font-medium">Twój wynik egzaminu</p>
        </div>

        <div className="flex justify-center items-center mb-8">
          <div className={`w-32 h-32 rounded-full flex items-center justify-center text-3xl font-black border-8 ${
            percentage >= 50 ? 'border-green-500 text-green-600' : 'border-red-500 text-red-600'
          }`}>
            {percentage}%
          </div>
        </div>

        <div className="max-w-xs mx-auto mb-8 bg-gray-50 p-4 rounded-2xl border border-gray-100 shadow-inner">
            <p className="text-[10px] text-gray-400 uppercase font-black tracking-widest mb-1">Punkty</p>
            <p className="text-3xl font-black text-gray-800">{result.punkty} / {total}</p>
        </div>

        <div className="flex flex-col md:flex-row gap-3">
          <Button className="flex-1" onClick={() => navigate(`/quiz`)}>Rozwiąż kolejny Quiz</Button>
          <Button variant="secondary" className="flex-1" onClick={() => navigate(`/kursy/${kursId}`)}>Wróć do Kursu</Button>
        </div>
      </Card>

      <div className="space-y-6">
          <h2 className="text-2xl font-black text-gray-800 border-l-4 border-indigo-600 pl-4">Przegląd odpowiedzi</h2>
          {result.wybrane.map((item, idx) => {
              const options = item.odpowiedzi || item.opcje_pytania || [];
              const questionIdInItem = options[0]?.pytanie_id;
              
              const originalQuestion = questions?.find(q => q.id === questionIdInItem);
              const questionText = originalQuestion?.tresc || `Pytanie #${questionIdInItem}`;
              
              const isUserCorrect = result.poprawne.includes(questionIdInItem);

              return (
                  <Card key={idx} className={`border-l-4 transition-all shadow-sm ${isUserCorrect ? 'border-l-green-500 bg-green-50/10' : 'border-l-red-500 bg-red-50/10'}`}>
                      <div className="flex justify-between items-start mb-4">
                          <span className="text-xs font-black text-gray-400 uppercase tracking-widest">Pytanie {idx + 1}</span>
                          <Badge color={isUserCorrect ? 'green' : 'red'}>{isUserCorrect ? 'DOBRZE' : 'BŁĄD'}</Badge>
                      </div>
                      <h3 className="text-lg font-bold text-gray-900 mb-6 leading-tight">{questionText}</h3>
                      
                      <div className="space-y-3">
                          {options.map((odp: Odpowiedz) => {
                              const isThisSelected = Number(odp.id) === Number(item.wybrana_opcja);
                              const isThisCorrect = odp.poprawna === true;
                              
                              let statusClass = "p-3 rounded-xl border text-sm flex justify-between items-center transition-all ";
                              
                              if (isThisSelected) {
                                  statusClass += isThisCorrect 
                                      ? "bg-green-100 border-green-500 text-green-800 font-bold shadow-md scale-[1.01]" 
                                      : "bg-red-100 border-red-500 text-red-800 font-bold shadow-md scale-[1.01]";
                              } else if (isThisCorrect) {
                                  statusClass += "bg-green-50 border-green-200 text-green-700 italic border-dashed";
                              } else {
                                  statusClass += "bg-white border-gray-100 opacity-60";
                              }

                              return (
                                  <div key={odp.id} className={statusClass}>
                                      <span className="pr-4">{odp.tresc}</span>
                                      <div className="flex items-center space-x-2 flex-shrink-0">
                                        {isThisSelected && (
                                            <span className="text-[9px] bg-white/80 px-2 py-0.5 rounded-full uppercase font-black text-gray-600 border border-gray-200 whitespace-nowrap shadow-sm">Twój wybór</span>
                                        )}
                                        {isThisCorrect && (
                                            <span className="text-[9px] bg-green-500 text-white px-2 py-0.5 rounded-full uppercase font-black shadow-sm whitespace-nowrap">Poprawna</span>
                                        )}
                                      </div>
                                  </div>
                              );
                          })}
                      </div>
                  </Card>
              );
          })}
      </div>
    </div>
  );
};