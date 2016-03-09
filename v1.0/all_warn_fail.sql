.headers on
SELECT DISTINCT
basic.filename, module_stats.overall, module_stats.per_base_sequence_quality, module_stats.per_tile_sequence_quality, module_stats.per_sequence_quality_scores, module_stats.per_base_sequence_content, module_stats.per_sequence_gc_content, module_stats.per_base_n_content, module_stats.sequence_length_distribution, module_stats.sequence_duplication_levels, module_stats.overrepresented_sequences, module_stats.adapter_content, module_stats.kmer_content
FROM basic, module_stats
WHERE (module_stats.overall = 'fail' OR module_stats.overall = 'warn'
OR module_stats.per_base_sequence_content = 'fail' OR module_stats.per_base_sequence_content = 'warn'
OR module_stats.per_tile_sequence_quality = 'fail' OR module_stats.per_tile_sequence_quality = 'warn'
OR module_stats.per_sequence_quality_scores = 'fail' OR module_stats.per_sequence_quality_scores = 'warn'
OR module_stats.per_base_sequence_content = 'fail' OR module_stats.per_base_sequence_content = 'warn'
OR module_stats.per_sequence_gc_content = 'fail' OR module_stats.per_sequence_gc_content = 'warn'
OR module_stats.per_base_n_content = 'fail' OR module_stats.per_base_n_content = 'warn'
OR module_stats.sequence_length_distribution = 'fail' OR module_stats.sequence_length_distribution = 'warn'
OR module_stats.sequence_duplication_levels = 'fail' OR module_stats.sequence_duplication_levels = 'warn'
OR module_stats.overrepresented_sequences = 'fail' OR module_stats.overrepresented_sequences = 'warn'
OR module_stats.adapter_content = 'fail' OR module_stats.adapter_content = 'warn'
OR module_stats.kmer_content = 'fail' OR module_stats.kmer_content = 'warn')
AND module_stats.id = basic.id
;
