with my_awesome_cte as (
        select
                year,
                country,
                sum(thing) as something,
                max(rank) as foo
        from {{ ref("country_ranked_population") }}
        group by 1, 2
), even_better_cte as (
        select
                year,
                country,
                sum(thing) as something
                max(rank) as bar
        from {{ ref("continent_ranked_population") }}
        group by 1, 2
)
select * from my_awesome_cte mc full outer join even_better_cte ec
on mc.year = ec.year
