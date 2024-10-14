    def key_result_area_score_card(self, quarter=None, year=None):
        cache_key = f"key_result_area_score_card_{self.pk}_{quarter}_{year}"
        result = cache.get(cache_key)
        if result is None:
            indicators = self.indicators.values_list('id', flat=True)  # Faster, no need for 'all()'

            score_query = AnnualPlan.objects if not quarter else QuarterProgress.objects

            filter_params = {
                'indicator__in': indicators,
                'year__year_amh': year
            }
            if quarter:
                filter_params['quarter__quarter_eng'] = quarter
                filter_params['quarter_target__isnull'] = False
                performance_field = 'quarter_performance'
                target_field = 'quarter_target'
            else:
                filter_params['annual_target__isnull'] = False
                performance_field = 'annual_performance'
                target_field = 'annual_target'
                # Perform a single query with necessary annotations and aggregations
                scores = score_query.filter(**filter_params).annotate(
    
                performance_value=Coalesce(F(performance_field), Value(0)),
                raw_performance_percentage=ExpressionWrapper(
                    F('performance_value') * 100.0 / F(target_field), output_field=FloatField()
                ),
                performance_percentage=Case(
                    When(raw_performance_percentage__gt=100, then=Value(100.0)),
                    default=F('raw_performance_percentage'),
                    output_field=FloatField()
                ),
                weighted_performance=ExpressionWrapper(
                    F('performance_percentage') * F('indicator__kpi_weight') / 100.0, 
                    output_field=FloatField()
                )
            ).aggregate(
                total_score=Sum('weighted_performance'),
                total_indicator_weight=Sum('indicator__kpi_weight'),
            )


            try:
                avg_score = float(scores['total_score'] * 100 / float(scores['total_indicator_weight'])) if scores['total_indicator_weight'] else 0
            except:
                avg_score = 0

    
            # Cache ScoreCardRanges only if necessary
            score_card_ranges = cache.get_or_set('score_card_ranges', lambda: list(ScoreCardRange.objects.all()), CACHE_TIMEOUT)
    
            card = next((range for range in score_card_ranges if range.starting <= avg_score <= range.ending), None)
            scorecard_color = card.color if card else "#4680ff"
    
            result = {
                'sum_score': avg_score,
                'avg_score': avg_score,
                'scorecard_color': scorecard_color,
            }
    
            cache.set(cache_key, result, CACHE_TIMEOUT)

        return result


    def ministry_key_result_area_score_card(self ,quarter=None, year=None , indicators_id=None):
        cache_key = f"ministry_key_result_area_score_card_{self.pk}_{quarter}_{year}"
        result = cache.get(cache_key)
        if result is None:
            indicators = self.indicators.filter(id__in=indicators_id).values_list('id', flat=True)

            if quarter:
                annual_scores = QuarterProgress.objects.filter(
                    Q(quarter_target__isnull=False),  
                    Q(indicator__in=indicators),
                    Q(year__year_amh=year),
                    Q(quarter__quarter_eng = quarter)
                ).annotate(
                    # Replace null performance values with 0 using Coalesce
                    performance_value=Coalesce('quarter_performance', Value(0)),
                    
                    # Calculate the percentage of performance over target for each row
                    raw_performance_percentage=ExpressionWrapper(
                        F('performance_value') * 100.0 / F('quarter_target'),
                        output_field=FloatField()
                    ),

                    
                    # Cap the performance percentage at 100 if it exceeds 100
                    performance_percentage=Case(
                        When(raw_performance_percentage__gt=100, then=Value(100.0)),
                        default=F('raw_performance_percentage'),
                        output_field=FloatField()
                    ),

                    kpi_weight_value=F('indicator__kpi_weight'),

                    weighted_performance=ExpressionWrapper(
                        F('performance_percentage') * (F('kpi_weight_value') / 100.0), 
                        output_field=FloatField()
                    )
                ).values('weighted_performance', 'kpi_weight_value'
                ).aggregate(
                    total_score=Sum('weighted_performance'),
                    total_indicator_weight=Sum('kpi_weight_value'),
                )

                sum_score = annual_scores['total_score'] or 0
                try: 
                    avg_score = float(annual_scores['total_score'] * 100) / float(annual_scores['total_indicator_weight']) 
                except: 
                    avg_score = 0
            else:
                annual_scores = AnnualPlan.objects.filter(
                    Q(annual_target__isnull=False),  
                    Q(indicator__in=indicators),
                    Q(year__year_amh=year)
                ).annotate(
                    # Replace null performance values with 0 using Coalesce
                    performance_value=Coalesce('annual_performance', Value(0)),
                    
                    # Calculate the percentage of performance over target for each row
                    raw_performance_percentage=ExpressionWrapper(
                        F('performance_value') * 100.0 / F('annual_target'),
                        output_field=FloatField()
                    ),

                    
                    # Cap the performance percentage at 100 if it exceeds 100
                    performance_percentage=Case(
                        When(raw_performance_percentage__gt=100, then=Value(100.0)),
                        default=F('raw_performance_percentage'),
                        output_field=FloatField()
                    ),

                    kpi_weight_value=F('indicator__kpi_weight'),

                    weighted_performance=ExpressionWrapper(
                        F('performance_percentage') * (F('kpi_weight_value') / 100.0), 
                        output_field=FloatField()
                    )
                ).values('weighted_performance', 'kpi_weight_value'
                ).aggregate(
                    total_score=Sum('weighted_performance'),
                    total_indicator_weight=Sum('kpi_weight_value'),
                )

                sum_score = annual_scores['total_score'] or 0
                try: 
                    avg_score = float(annual_scores['total_score'] * 100) / float(annual_scores['total_indicator_weight']) 
                except: 
                    avg_score = 0
                    


            score_card_ranges = cache.get('score_card_ranges')
            if score_card_ranges is None:
                score_card_ranges = list(ScoreCardRange.objects.all())
                cache.set('score_card_ranges', score_card_ranges, CACHE_TIMEOUT)

            card = next((range for range in score_card_ranges if range.starting <= avg_score <= range.ending), None)
            scorecard_color = card.color if card else "#4680ff"

            result = {
                'sum_score': sum_score,
                'avg_score': avg_score,
                'scorecard_color': scorecard_color,
            }
            cache.set(cache_key, result, CACHE_TIMEOUT)

        return result
