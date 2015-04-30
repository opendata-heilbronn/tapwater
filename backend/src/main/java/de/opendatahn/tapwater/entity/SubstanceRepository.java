package de.opendatahn.tapwater.entity;

import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface SubstanceRepository extends JpaRepository<Substance, Long> {

	List<Substance> findBySubarea(Subarea subarea);
}
