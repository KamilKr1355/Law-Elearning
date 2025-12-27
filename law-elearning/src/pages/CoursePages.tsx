
import React, { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { kursService, aktywnoscService, contentAdminService, wynikiService } from '../services/api';
import type { Kurs, Rozdzial, ArtykulView, Komentarz, Notatka, Pytanie, Odpowiedz, OcenaArtykuluCombined, KursProgress, StatystykiPytania, ZapisArtykulu } from '../types';
import { Card, Button, Spinner, Badge, Input, ConfirmationModal } from '../components/UI';
import { useAuth } from '../context/AuthContext';
import { isUserAdmin } from '../utils/auth';

export const KursyList = () => {
  const [kursy, setKursy] = useState<Kurs[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    kursService.getAll()
      .then(setKursy)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <Spinner />;

  const filteredKursy = kursy.filter(k => 
    k.nazwa_kursu.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row justify-between items-center gap-4">
        <h1 className="text-3xl font-bold text-gray-900">Dostępne Kursy</h1>
        <div className="relative">
          <input 
            type="text" 
            placeholder="Szukaj kursu..." 
            className="pl-10 pr-4 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
          <span className="absolute left-3 top-2.5 text-gray-400">🔍</span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredKursy.map((kurs) => (
          <Link key={kurs.id} to={`/kursy/${kurs.id}`}>
            <Card hover className="h-full flex flex-col justify-between">
              <div>
                <div className="text-4xl mb-4">🎓</div>
                <h3 className="text-xl font-bold text-gray-900 mb-2">{kurs.nazwa_kursu}</h3>
                <p className="text-gray-500 text-sm">Kliknij, aby rozpocząć naukę.</p>
              </div>
              <div className="mt-4 flex justify-end">
                <span className="text-indigo-600 font-medium text-sm">Przejdź do kursu &rarr;</span>
              </div>
            </Card>
          </Link>
        ))}
        {filteredKursy.length === 0 && (
          <div className="col-span-full text-center py-10 text-gray-500">
            Nie znaleziono kursów pasujących do wyszukiwania.
          </div>
        )}
      </div>
    </div>
  );
};

export const KursDetail = () => {
  const { id } = useParams<{ id: string }>();
  const [kurs, setKurs] = useState<Kurs | null>(null);
  const [rozdzialy, setRozdzialy] = useState<Rozdzial[]>([]);
  const [articlesByChapter, setArticlesByChapter] = useState<{ [key: number]: ArtykulView[] }>({});
  const [expandedChapters, setExpandedChapters] = useState<{ [key: number]: boolean }>({});
  const [progressData, setProgressData] = useState<KursProgress | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (id) {
      const loadData = async () => {
        setLoading(true);
        try {
          const [k, r, p] = await Promise.all([
            kursService.getOne(id),
            kursService.getRozdzialy(id),
            aktywnoscService.getPostepKursu(id).catch(() => null)
          ]);
          
          const courseData = Array.isArray(k) ? k[0] : k;
          setKurs(courseData);
          setRozdzialy(r);
          if (p) setProgressData(p);

          const artsMapping: { [key: number]: ArtykulView[] } = {};
          
          await Promise.all(r.map(async (rozdzial: Rozdzial) => {
             try {
               const arts = await kursService.getArtykulyByRozdzial(rozdzial.id);
               artsMapping[rozdzial.id] = Array.isArray(arts) ? arts : [];
             } catch (error) {
               artsMapping[rozdzial.id] = [];
             }
          }));

          setArticlesByChapter(artsMapping);

        } catch (e) {
          console.error("Błąd ładowania kursu", e);
        } finally {
          setLoading(false);
        }
      };

      loadData();
    }
  }, [id]);

  const toggleChapter = (chapterId: number) => {
    setExpandedChapters(prev => ({
      ...prev,
      [chapterId]: !prev[chapterId]
    }));
  };

  if (loading) return <Spinner />;
  if (!kurs) return <div className="text-center p-10">Nie znaleziono kursu.</div>;

  return (
    <div className="space-y-8">
      <div>
        <div className="flex justify-between items-end mb-4">
            <div>
                <h1 className="text-3xl font-bold text-gray-900">{kurs.nazwa_kursu}</h1>
                <p className="mt-2 text-gray-600">Rozwiń rozdział, aby zobaczyć listę artykułów.</p>
            </div>
            {progressData && (
                 <div className="text-right">
                     <span className="text-sm font-bold text-indigo-600">{progressData.podsumowanie.progress_percentage.toFixed(0)}% Ukończono</span>
                 </div>
            )}
        </div>
        
        {progressData && (
            <div className="w-full bg-gray-200 rounded-full h-2.5 mb-6">
                <div 
                    className="bg-indigo-600 h-2.5 rounded-full transition-all duration-500" 
                    style={{ width: `${progressData.podsumowanie.progress_percentage}%` }}
                ></div>
            </div>
        )}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 space-y-4">
          {rozdzialy.length === 0 ? (
            <div className="text-gray-500">Brak rozdziałów w tym kursie.</div>
          ) : (
            rozdzialy.map((rozdzial) => {
              const isExpanded = !!expandedChapters[rozdzial.id];
              const arts = articlesByChapter[rozdzial.id] || [];
              
              return (
                <div key={rozdzial.id} className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
                  <button 
                    onClick={() => toggleChapter(rozdzial.id)}
                    className="w-full flex items-center justify-between p-4 text-left hover:bg-gray-50 transition-colors focus:outline-none"
                  >
                    <h3 className="text-lg font-bold text-gray-800">{rozdzial.nazwa_rozdzialu}</h3>
                    <div className="flex items-center space-x-3">
                        <span className="text-xs font-medium text-gray-400 bg-gray-100 px-2 py-1 rounded-full">{arts.length} art.</span>
                        <span className={`transform transition-transform duration-200 ${isExpanded ? 'rotate-180' : ''}`}>▼</span>
                    </div>
                  </button>
                  
                  {isExpanded && (
                    <div className="p-4 bg-gray-50 border-t border-gray-100 space-y-2 animate-fadeIn">
                       {arts.length > 0 ? (
                         arts.map((art) => {
                          const realId = art.id || art.artykul_id;
                          return (
                            <Link key={realId} to={`/artykul/${realId}`} className="block">
                              <div className="p-3 rounded-lg bg-white hover:bg-indigo-50 hover:text-indigo-700 transition flex justify-between items-center group cursor-pointer border border-gray-200 shadow-sm">
                                <div className="flex items-center space-x-3">
                                  {art.nr_artykulu && (
                                    <span className="text-xs font-bold bg-indigo-100 text-indigo-700 px-2 py-0.5 rounded">
                                      Art. {art.nr_artykulu}
                                    </span>
                                  )}
                                  <span className="font-medium text-sm text-gray-700 group-hover:text-indigo-700">
                                    {art.tytul || `Artykuł #${realId}`}
                                  </span>
                                </div>
                                <span className="text-gray-400 group-hover:text-indigo-500 text-xs">Czytaj &rarr;</span>
                              </div>
                            </Link>
                          );
                         })
                       ) : (
                          <span className="text-sm text-gray-400 italic">Brak artykułów w tym rozdziale.</span>
                       )}
                    </div>
                  )}
                </div>
              );
            })
          )}
        </div>
        
        <div>
           <Card className="sticky top-24 bg-indigo-50 border-indigo-100 space-y-4">
              <h3 className="font-bold text-indigo-900 border-b border-indigo-200 pb-2">Tryby Nauki</h3>
              
              <Link to={`/nauka/${id}`} className="block">
                  <div className="bg-white p-4 rounded-lg shadow-sm hover:shadow-md transition cursor-pointer border border-indigo-100 flex items-center space-x-3 group">
                      <span className="text-2xl group-hover:scale-110 transition">🧠</span>
                      <div>
                          <h4 className="font-bold text-gray-800">Fiszki / Nauka</h4>
                          <p className="text-xs text-gray-500">Powtarzaj materiał</p>
                      </div>
                  </div>
              </Link>

              <Link to={`/quiz?kursId=${id}`} className="block">
                  <div className="bg-white p-4 rounded-lg shadow-sm hover:shadow-md transition cursor-pointer border border-indigo-100 flex items-center space-x-3 group">
                      <span className="text-2xl group-hover:scale-110 transition">📝</span>
                      <div>
                          <h4 className="font-bold text-gray-800">Egzamin Próbny</h4>
                          <p className="text-xs text-gray-500">Sprawdź wiedzę</p>
                      </div>
                  </div>
              </Link>

              <div className="pt-2">
                <Link to={`/kursy/${id}/notatki`} className="block">
                    <div className="bg-amber-50 p-4 rounded-lg shadow-sm hover:shadow-md transition cursor-pointer border border-amber-200 flex items-center space-x-3 group">
                        <span className="text-2xl group-hover:scale-110 transition">📌</span>
                        <div>
                            <h4 className="font-bold text-amber-900">Notatki z Kursu</h4>
                            <p className="text-xs text-amber-700">Twoje własne notatki</p>
                        </div>
                    </div>
                </Link>
              </div>
           </Card>
        </div>
      </div>
    </div>
  );
};

export const ArtykulReader = () => {
  const { id } = useParams<{ id: string }>();
  const [artykul, setArtykul] = useState<ArtykulView | null>(null);
  const [loading, setLoading] = useState(true);
  
  const [komentarze, setKomentarze] = useState<Komentarz[]>([]);
  const [newComment, setNewComment] = useState('');
  
  const [deleteModalOpen, setDeleteModalOpen] = useState(false);
  const [commentToDelete, setCommentToDelete] = useState<number | null>(null);

  const [editingCommentId, setEditingCommentId] = useState<number | null>(null);
  const [editingText, setEditingText] = useState('');
  
  const [isSaved, setIsSaved] = useState(false);
  
  const [ratingData, setRatingData] = useState<OcenaArtykuluCombined | null>(null);
  const [userRating, setUserRating] = useState(0);

  const [questions, setQuestions] = useState<Pytanie[]>([]);
  const [expandedQuestions, setExpandedQuestions] = useState<{ [key: number]: boolean }>({});
  const [selectedAnswers, setSelectedAnswers] = useState<{ [key: number]: number }>({});
  const [questionStats, setQuestionStats] = useState<{ [key: number]: StatystykiPytania }>({});

  const [noteContent, setNoteContent] = useState('');
  const [noteSaving, setNoteSaving] = useState(false);
  const [noteMessage, setNoteMessage] = useState('');

  const { user } = useAuth();

  useEffect(() => {
    if (id && id !== 'undefined') {
      setLoading(true);
      
      const loadInitial = async () => {
         try {
             const art = await kursService.getArtykulDetail(id);
             setArtykul(art);
             
             try {
                const kom = await aktywnoscService.getKomentarze(id);
                setKomentarze(Array.isArray(kom) ? kom : []);
             } catch (e) {
                 setKomentarze([]);
             }

             try {
                 const savedStatus = await aktywnoscService.checkZapis(id);
                 setIsSaved(savedStatus);
             } catch (e) {
                 setIsSaved(false);
             }

             try {
                 const ocena = await aktywnoscService.getOcena(id);
                 setRatingData(ocena);
                 if (ocena && ocena.moja_ocena) {
                     setUserRating(ocena.moja_ocena.ocena);
                 }
             } catch (e) {}

             try {
                 const qs = await contentAdminService.getPytaniaByArtykul(parseInt(id));
                 if (Array.isArray(qs)) {
                     setQuestions(qs);
                 }
             } catch (e) {}

         } catch (e) {
             console.error(e);
         } finally {
             setLoading(false);
         }
      };
      
      loadInitial();
    } else {
        setLoading(false);
    }
  }, [id]);

  const handleToggleSave = async () => {
      if (!id) return;
      const articleId = parseInt(id);
      
      try {
        if (isSaved) {
            await aktywnoscService.deleteZapis(articleId);
            setIsSaved(false);
        } else {
            await aktywnoscService.addZapis(articleId);
            setIsSaved(true);
        }
      } catch (e) {
          console.error("Błąd podczas zmiany statusu zapisu", e);
      }
  };

  const handleAddComment = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!id || !newComment.trim()) return;
    try {
      await aktywnoscService.addKomentarz(id, newComment);
      const updated = await aktywnoscService.getKomentarze(id);
      setKomentarze(Array.isArray(updated) ? updated : []);
      setNewComment('');
    } catch (error) {
      alert('Błąd dodawania komentarza');
    }
  };

  const handleDeleteClick = (commentId: number) => {
      setCommentToDelete(commentId);
      setDeleteModalOpen(true);
  };

  const confirmDeleteComment = async () => {
      if (commentToDelete === null) return;
      try {
          await aktywnoscService.deleteKomentarz(commentToDelete);
          setKomentarze(prev => prev.filter(k => k.id !== commentToDelete));
      } catch (e) {
          console.error("Delete failed", e);
      } finally {
          setDeleteModalOpen(false);
          setCommentToDelete(null);
      }
  };

  const handleStartEdit = (comment: Komentarz) => {
      setEditingCommentId(comment.id);
      setEditingText(comment.tresc);
  };

  const handleCancelEdit = () => {
      setEditingCommentId(null);
      setEditingText('');
  };

  const handleSaveEdit = async (commentId: number) => {
      if (!editingText.trim()) return;
      try {
          await aktywnoscService.updateKomentarz(commentId, editingText);
          setKomentarze(prev => prev.map(c => c.id === commentId ? { ...c, tresc: editingText } : c));
          setEditingCommentId(null);
          setEditingText('');
      } catch (e) {
          console.error(e);
          alert('Nie udało się zaktualizować komentarza.');
      }
  };

  const handleRate = async (rate: number) => {
      if (!id) return;
      setUserRating(rate);
      try {
          await aktywnoscService.setOcena(id, rate);
          const freshStats = await aktywnoscService.getOcena(id);
          setRatingData(freshStats);
      } catch (e) {
          console.error(e);
      }
  };

  const toggleQuestionExpand = async (qId: number) => {
      const isExpanded = !!expandedQuestions[qId];
      setExpandedQuestions(prev => ({ ...prev, [qId]: !isExpanded }));

      const qIndex = questions.findIndex(q => q.id === qId);
      if (!isExpanded && qIndex !== -1 && !questions[qIndex].odpowiedzi) {
          try {
              const answers = await contentAdminService.getOdpowiedzi(qId);
              setQuestions(prev => {
                  const copy = [...prev];
                  copy[qIndex] = { ...copy[qIndex], odpowiedzi: answers };
                  return copy;
              });
          } catch (e) {
              console.error("Błąd pobierania odpowiedzi", e);
          }
      }
  };

  const handleSelectAnswer = async (qId: number, ansId: number, isCorrect: boolean) => {
      if (selectedAnswers[qId]) return;
      
      setSelectedAnswers(prev => ({ ...prev, [qId]: ansId }));

      try {
          await aktywnoscService.updatePostepNauki({
              pytanie_id: qId,
              is_correct: isCorrect
          });
          
          const stats = await wynikiService.getStats(qId);
          setQuestionStats(prev => ({ ...prev, [qId]: stats }));
      } catch (e) {
          console.error(e);
      }
  };

  const handleSaveNote = async () => {
    if (!id || !noteContent.trim()) return;
    setNoteSaving(true);
    try {
      await aktywnoscService.addNotatka({
        tresc: noteContent,
        artykul_id: parseInt(id)
      });
      setNoteMessage('Notatka zapisana!');
      setNoteContent('');
      setTimeout(() => setNoteMessage(''), 3000);
    } catch (error) {
      console.error(error);
      setNoteMessage('Błąd zapisu.');
    } finally {
      setNoteSaving(false);
    }
  };

  if (loading) return <Spinner />;
  if (!artykul) return <div className="p-8 text-center text-gray-500">Nie znaleziono artykułu lub błędny adres.</div>;

  return (
    <>
      <ConfirmationModal 
        isOpen={deleteModalOpen}
        onClose={() => setDeleteModalOpen(false)}
        onConfirm={confirmDeleteComment}
        title="Usuwanie komentarza"
        message="Czy na pewno chcesz usunąć ten komentarz? Tej operacji nie można cofnąć."
      />

      <div className="max-w-4xl mx-auto grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2">
          <Card className="mb-8">
            <div className="flex justify-between items-start mb-4">
               <div>
                  <div className="flex items-center space-x-2 mb-1">
                      {artykul.nr_artykulu && <Badge color="blue">Art. {artykul.nr_artykulu}</Badge>}
                  </div>
                  <h1 className="text-2xl font-bold">{artykul.tytul || `Artykuł ${artykul.id}`}</h1>
                  <div className="flex items-center space-x-2 mt-2">
                      <div className="flex text-yellow-400">
                          {[1, 2, 3, 4, 5].map(star => (
                              <button 
                                  key={star} 
                                  onClick={() => handleRate(star)}
                                  className={`focus:outline-none transition transform hover:scale-110 ${star <= userRating ? 'opacity-100' : 'opacity-30'}`}
                              >
                                  ★
                              </button>
                          ))}
                      </div>
                      <span className="text-xs text-gray-500">
                          (Średnia: {ratingData?.srednia_ocena ? parseFloat(ratingData.srednia_ocena.toString()).toFixed(1) : '0.0'})
                      </span>
                  </div>
               </div>
               <button onClick={handleToggleSave} className={`text-2xl transition hover:scale-110 ${isSaved ? 'text-yellow-400' : 'text-gray-300'}`} title={isSaved ? "Usuń z zapisanych" : "Zapisz na później"}>
                   {isSaved ? '★' : '☆'}
               </button>
            </div>
            <div className="prose max-w-none text-gray-700 leading-relaxed border-t pt-4">
              <div dangerouslySetInnerHTML={{ __html: artykul.tresc }} />
            </div>
          </Card>

          <div className="mb-8">
              <h3 className="text-lg font-bold text-gray-800 mb-4 flex items-center">
                  <span>Sprawdź wiedzę</span>
                  <span className="ml-2 text-xs bg-indigo-100 text-indigo-700 px-2 py-1 rounded-full">{questions.length} pytań</span>
              </h3>

              <div className="space-y-3">
                  {questions.length === 0 ? (
                      <p className="text-gray-500 italic">Brak pytań do tego artykułu.</p>
                  ) : (
                      questions.map((q, idx) => {
                          const isExpanded = expandedQuestions[q.id];
                          const selectedAnsId = selectedAnswers[q.id];
                          const stats = questionStats[q.id];

                          return (
                              <div key={q.id} className="bg-white border border-gray-200 rounded-lg overflow-hidden transition-all shadow-sm">
                                  <button 
                                      onClick={() => toggleQuestionExpand(q.id)}
                                      className="w-full text-left p-4 bg-gray-50 hover:bg-gray-100 flex justify-between items-center font-medium text-gray-800 focus:outline-none"
                                  >
                                      <span>{idx + 1}. {q.tresc}</span>
                                      <span className={`transform transition-transform ${isExpanded ? 'rotate-180' : ''}`}>▼</span>
                                  </button>
                                  
                                  {isExpanded && (
                                      <div className="p-4 border-t border-gray-100 bg-white animate-fadeIn">
                                          {!q.odpowiedzi ? (
                                              <div className="text-center py-2"><Spinner /></div>
                                          ) : q.odpowiedzi.length === 0 ? (
                                              <p className="text-sm text-gray-400">Brak zdefiniowanych odpowiedzi.</p>
                                          ) : (
                                              <div className="space-y-2">
                                                  {q.odpowiedzi.map(odp => {
                                                      let btnClass = "w-full text-left p-3 rounded border text-sm transition-all ";
                                                      
                                                      if (selectedAnsId) {
                                                          if (odp.poprawna) {
                                                              btnClass += "bg-green-100 border-green-500 text-green-800 font-semibold";
                                                          } else if (selectedAnsId === odp.id && !odp.poprawna) {
                                                              btnClass += "bg-red-100 border-red-500 text-red-800";
                                                          } else {
                                                              btnClass += "bg-gray-50 border-gray-100 opacity-50";
                                                          }
                                                      } else {
                                                          btnClass += "bg-white border-gray-200 hover:border-indigo-400 hover:bg-indigo-50";
                                                      }

                                                      return (
                                                          <button 
                                                              key={odp.id}
                                                              onClick={() => handleSelectAnswer(q.id, odp.id, odp.poprawna)}
                                                              disabled={!!selectedAnsId}
                                                              className={btnClass}
                                                          >
                                                              {odp.tresc}
                                                              {selectedAnsId && odp.poprawna && <span className="float-right font-bold">✓ Poprawna</span>}
                                                              {selectedAnsId === odp.id && !odp.poprawna && <span className="float-right font-bold">✕ Twoja</span>}
                                                          </button>
                                                      );
                                                  })}
                                              </div>
                                          )}
                                          
                                          {selectedAnsId && stats && (
                                              <div className="mt-3 text-xs text-center text-gray-500 bg-gray-50 p-2 rounded">
                                                  Statystyki: <span className="font-bold text-indigo-600">{parseFloat(stats.procent_poprawnych).toFixed(0)}%</span> użytkowników odpowiedziało poprawnie na to pytanie.
                                              </div>
                                          )}
                                      </div>
                                  )}
                              </div>
                          );
                      })
                  )}
              </div>
          </div>

          <div className="mt-8 border-t pt-8">
            <h3 className="text-xl font-bold mb-4">Komentarze ({komentarze.length})</h3>
            {user && (
              <form onSubmit={handleAddComment} className="mb-6">
                <textarea 
                  className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none"
                  placeholder="Dodaj komentarz..."
                  rows={3}
                  value={newComment}
                  onChange={(e) => setNewComment(e.target.value)}
                />
                <div className="flex justify-end mt-2">
                  <Button type="submit">Wyślij</Button>
                </div>
              </form>
            )}
            <div className="space-y-4">
              {komentarze.map((k) => (
                <div key={k.id} className="bg-white p-4 rounded-lg shadow-sm border border-gray-100 relative group">
                  <div className="flex justify-between items-start mb-2">
                    <span className="font-semibold text-gray-900">{k.username || 'Użytkownik'}</span>
                    <div className="flex items-center space-x-2">
                        {user && (user.username === k.username || isUserAdmin(user)) && !editingCommentId && (
                          <div className="flex space-x-1 opacity-0 group-hover:opacity-100 transition">
                              {user.username === k.username && (
                                  <button 
                                      onClick={() => handleStartEdit(k)}
                                      className="text-gray-400 hover:text-indigo-600 p-1 rounded hover:bg-indigo-50 transition"
                                      title="Edytuj komentarz"
                                  >
                                      ✎
                                  </button>
                              )}
                              <button 
                                  onClick={() => handleDeleteClick(k.id)}
                                  className="text-gray-400 hover:text-red-500 p-1 rounded hover:bg-red-50 transition"
                                  title="Usuń komentarz"
                              >
                                  🗑
                              </button>
                          </div>
                        )}

                        <span className="text-xs text-gray-500">
                          {k.data_zapisu ? new Date(k.data_zapisu).toLocaleDateString() : ''}
                        </span>
                    </div>
                  </div>
                  
                  {editingCommentId === k.id ? (
                      <div className="mt-2 animate-fadeIn">
                          <textarea 
                              className="w-full p-2 border rounded-lg text-sm mb-2 focus:ring-2 focus:ring-indigo-500 outline-none" 
                              rows={3}
                              value={editingText}
                              onChange={(e) => setEditingText(e.target.value)}
                          />
                          <div className="flex space-x-2 justify-end">
                              <Button variant="secondary" onClick={handleCancelEdit} className="text-xs py-1">Anuluj</Button>
                              <Button onClick={() => handleSaveEdit(k.id)} className="text-xs py-1">Zapisz</Button>
                          </div>
                      </div>
                  ) : (
                      <p className="text-gray-700 text-sm">{k.tresc}</p>
                  )}
                </div>
              ))}
              {komentarze.length === 0 && <p className="text-gray-500 text-sm">Brak komentarzy. Bądź pierwszy!</p>}
            </div>
          </div>
        </div>

        <div className="space-y-6">
          <Card>
             <h3 className="font-bold text-gray-900 mb-3">Twoje Notatki</h3>
             <textarea 
               className="w-full h-32 p-2 text-sm border rounded bg-yellow-50 border-yellow-200 outline-none focus:ring-1 focus:ring-yellow-400" 
               placeholder="Wpisz notatkę do tego artykułu..."
               value={noteContent}
               onChange={(e) => setNoteContent(e.target.value)}
             ></textarea>
             <Button 
               variant="secondary" 
               className="w-full mt-2 text-sm"
               onClick={handleSaveNote}
               disabled={noteSaving}
             >
               {noteSaving ? 'Zapisywanie...' : 'Zapisz notatkę'}
             </Button>
             {noteMessage && <p className="text-xs text-center mt-2 text-green-600 font-bold">{noteMessage}</p>}
             <div className="mt-4 text-center">
               <Link to="/moje-notatki" className="text-xs text-indigo-600 hover:underline">Zobacz wszystkie notatki</Link>
             </div>
          </Card>
        </div>
      </div>
    </>
  );
};
