package de.opendatahn.tapwater.entity;


import javax.persistence.*;

@Entity
public class City {

	@Id
	@GeneratedValue
	private Long id;

	@Column(nullable = false)
	private String name;

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public Long getId() {
		return id;
	}

	public void setId(Long id) {
		this.id = id;
	}
}
