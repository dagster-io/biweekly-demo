with my_awesome_cte as (
        select
                country,
                sum(pop_2018) as something,
                max(pop_2019) as foo
        from {{ ref("country_ranked_population") }}
        group by 1
), even_better_cte as (
        select
                sum(pop_2018) as something,
                max(pop_2019) as bar
        from {{ ref("continent_ranked_population") }}
)
select * from my_awesome_cte
