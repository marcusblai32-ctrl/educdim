# ============================================
# LECON (KORIJE - SANS QUIZ)
# ============================================
class Lecon(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lecons', verbose_name="Module")
    titre = models.CharField(max_length=255, verbose_name="Titre")
    description = models.TextField(blank=True, verbose_name="Description")
    contenu = models.TextField(blank=True, verbose_name="Contenu texte")
    ordre = models.PositiveIntegerField(default=1, verbose_name="Ordre")
    actif = models.BooleanField(default=True, verbose_name="Actif")
    # quiz = models.ForeignKey('quiz.Quiz', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Quiz associé")  # <--- RETIRE

    class Meta:
        verbose_name = "Leçon"
        verbose_name_plural = "Leçons"
        ordering = ['module', 'ordre']

    def __str__(self):
        return f"{self.module} - Leçon {self.ordre}: {self.titre}"
